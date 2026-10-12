from datetime import timedelta
from urllib.parse import parse_qs

from django.http import QueryDict
from django.urls import reverse
from django.utils import timezone

from tickets import queries
from tickets.constants import Status
from tickets.models import Category, Ticket

from .helpers import FoundationCase


class TicketQueryTests(FoundationCase):
    def page(self, parameters="", actor=None):
        return queries.ticket_list_page(actor or self.itadmin, QueryDict(parameters))

    def test_case_insensitive_search_uses_title_or_description(self):
        title = self.make_ticket(title="WiFi unavailable")
        body = self.make_ticket(title="Laptop issue", description="WiFi drops on calls")
        self.make_ticket(title="Printer issue")
        self.assertEqual({t.pk for t in self.page("q=wIfI")["tickets"]}, {title.pk, body.pk})
        self.assertEqual(list(self.page("q=missing")["tickets"]), [])
        self.assertEqual(self.page("q=%20%20")["page_obj"].paginator.count, 3)

    def test_combined_and_filters_and_explicit_related_name_query(self):
        other_category = Category.objects.create(name="Network")
        matching = self.make_ticket(title="VPN unavailable", category=other_category, priority="high", status=Status.ASSIGNED, assigned_to=self.technician)
        self.make_ticket(title="VPN unavailable", category=other_category, priority="low", status=Status.ASSIGNED, assigned_to=self.technician)
        self.make_ticket(title="VPN unavailable", priority="high")
        result = self.page(f"q=vpn&category={other_category.pk}&priority=high&status=assigned&order=oldest")
        self.assertEqual(list(result["tickets"]), [matching])
        self.assertIn('"tickets_category"."name"', str(result["tickets"].query))
        self.assertEqual(parse_qs(result["filter_query"]), {"q": ["vpn"], "category": [str(other_category.pk)], "priority": ["high"], "status": ["assigned"], "order": ["oldest"]})

    def test_priority_order_uses_business_rank_and_deterministic_ties(self):
        tickets = [self.make_ticket(priority=priority) for priority in ("medium", "low", "high", "high", "medium")]
        Ticket.objects.update(created_at=timezone.now())
        result = list(self.page("order=priority")["tickets"])
        self.assertEqual([t.pk for t in result], [tickets[3].pk, tickets[2].pk, tickets[4].pk, tickets[0].pk, tickets[1].pk])

    def test_newest_oldest_updated_and_tie_breakers(self):
        tickets = [self.make_ticket() for _ in range(3)]
        now = timezone.now()
        Ticket.objects.update(created_at=now, updated_at=now)
        self.assertEqual([t.pk for t in self.page()["tickets"]], [t.pk for t in reversed(tickets)])
        self.assertEqual([t.pk for t in self.page("order=oldest")["tickets"]], [t.pk for t in tickets])
        Ticket.objects.filter(pk=tickets[0].pk).update(updated_at=now + timedelta(minutes=1))
        self.assertEqual([t.pk for t in self.page("order=updated")["tickets"]], [tickets[0].pk, tickets[2].pk, tickets[1].pk])

    def test_invalid_parameters_are_ignored_independently_and_never_preserved(self):
        matching = self.make_ticket(priority="high", title="VPN issue")
        self.make_ticket(priority="low")
        for bad in ("status=unknown", "category=garbage", "category=999999", "order=__password", "q=" + "x" * 201):
            result = self.page("priority=high&" + bad + "&unexpected=value")
            self.assertEqual(list(result["tickets"]), [matching])
            self.assertTrue(result["filter_form"].errors)
            preserved = parse_qs(result["filter_query"])
            self.assertEqual(preserved["priority"], ["high"])
            self.assertNotIn("unexpected", preserved)
            self.assertEqual(preserved["order"], ["newest"])
        self.assertTrue(self.page("priority=urgent")["filter_form"].errors)

    def test_repeated_values_are_ignored_without_discarding_valid_filters(self):
        high = self.make_ticket(priority="high")
        self.make_ticket(priority="low")
        for repeated in ("status=new&status=resolved", "q=printer&q=network", "category=1&category=2", "order=oldest&order=priority"):
            result = self.page("priority=high&" + repeated)
            self.assertEqual(list(result["tickets"]), [high])
            self.assertTrue(result["filter_form"].errors)

    def test_pagination_ten_per_page_all_boundaries_and_invalid_numbers(self):
        tickets = [self.make_ticket() for _ in range(23)]
        for value, expected_page, expected_count in (("1", 1, 10), ("2", 2, 10), ("3", 3, 3), ("4", 3, 3),
            ("-1", 1, 10), ("0", 1, 10), ("abc", 1, 10), ("", 1, 10), ("1.5", 1, 10), ("9" * 5000, 1, 10)):
            result = self.page("page=" + value)
            self.assertEqual(result["page_obj"].number, expected_page)
            self.assertEqual(len(result["tickets"]), expected_count)
        self.assertEqual(self.page("page=2&page=3")["page_obj"].number, 1)
        all_ids = [t.pk for page in range(1, 4) for t in self.page(f"page={page}")["tickets"]]
        self.assertEqual(all_ids, [t.pk for t in reversed(tickets)])
        self.assertEqual(len(set(all_ids)), 23)

    def test_empty_queryset_has_valid_first_page(self):
        for parameters in ("", "page=99", "q=nope&page=-1"):
            result = self.page(parameters)
            self.assertEqual(result["page_obj"].number, 1)
            self.assertEqual(result["page_obj"].paginator.count, 0)

    def test_role_scope_survives_search_filters_order_and_pagination(self):
        for _ in range(11):
            self.make_ticket(title="Scoped VPN", priority="high", assigned_to=self.technician, status=Status.ASSIGNED)
        hidden = self.make_ticket(title="Hidden VPN", requester=self.other, priority="high", assigned_to=self.technician2, status=Status.ASSIGNED)
        params = f"q=vpn&status=assigned&priority=high&category={self.category.pk}&order=priority&page=2"
        for actor in (self.employee, self.technician):
            result = self.page(params, actor)
            self.assertEqual(result["page_obj"].paginator.count, 11)
            self.assertNotIn(hidden.pk, [t.pk for t in result["tickets"]])
        self.assertEqual(self.page(params, self.itadmin)["page_obj"].paginator.count, 12)

    def test_http_preserves_only_valid_parameters_and_selected_controls(self):
        for _ in range(12):
            self.make_ticket(title="VPN & email", priority="high")
        self.client.force_login(self.employee)
        response = self.client.get(reverse("tickets:ticket_list"), {"q": "VPN &", "priority": "high", "category": self.category.pk,
                                                                  "order": "oldest", "status": "invalid", "junk": "secret"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid filters were ignored")
        self.assertContains(response, "Page 1 of 2")
        self.assertContains(response, 'value="oldest" selected')
        self.assertContains(response, "page=2")
        params = parse_qs(response.context["filter_query"])
        self.assertEqual(params["q"], ["VPN &"])
        self.assertNotIn("status", params)
        self.assertNotIn("junk", params)
        next_response = self.client.get(reverse("tickets:ticket_list") + "?" + response.context["filter_query"] + "&page=2")
        self.assertEqual(len(next_response.context["tickets"]), 2)
        self.assertEqual(next_response.context["page_obj"].number, 2)

    def test_http_no_result_and_initial_empty_states_are_distinct(self):
        self.client.force_login(self.employee)
        self.assertContains(self.client.get(reverse("tickets:ticket_list")), "No tickets yet")
        self.assertContains(self.client.get(reverse("tickets:ticket_list"), {"q": "missing"}), "No matching tickets")

    def test_category_filter_tracks_renames_and_ticket_values_are_escaped(self):
        ticket = self.make_ticket(title="<script>device</script>")
        self.category.name = "New classification"
        self.category.full_clean()
        self.category.save()
        self.assertEqual(list(self.page(f"category={self.category.pk}")["tickets"]), [ticket])
        self.client.force_login(self.employee)
        self.assertContains(self.client.get(reverse("tickets:ticket_list")), "&lt;script&gt;device&lt;/script&gt;")
