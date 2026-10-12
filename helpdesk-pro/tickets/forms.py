"""Explicit user-editable fields; workflow metadata is supplied by services."""

from django import forms

from .constants import Priority, Status
from .models import Category, Ticket
from .permissions import eligible_technicians


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description", "category", "department", "priority")
        widgets = {"description": forms.Textarea(attrs={"rows": 7})}
        help_texts = {
            "title": "Briefly describe the issue (up to 150 characters).",
            "description": "Include what happened, the impact and anything you have already tried.",
            "department": "Choose the department requesting support for this issue.",
            "priority": "Low: minor inconvenience. Medium: work affected. High: work blocked.",
        }


class AssignmentForm(forms.Form):
    assigned_to = forms.ModelChoiceField(queryset=None, label="Technician", empty_label="Choose a technician")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assigned_to"].queryset = eligible_technicians()


class ResolutionForm(forms.Form):
    resolution_note = forms.CharField(
        label="Resolution note", strip=True,
        widget=forms.Textarea(attrs={"rows": 4}),
        help_text="Explain the fix and outcome. Resolving makes this ticket read-only.",
    )


class CommentForm(forms.Form):
    body = forms.CharField(label="Comment", strip=True, widget=forms.Textarea(attrs={"rows": 4}),
                           help_text="Comments are visible to the requester and IT team and cannot be edited or deleted.")


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "description")
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}
        help_texts = {"name": "A unique category name, up to 100 characters.",
                      "description": "Optional guidance for choosing this category."}


class TicketFilterForm(forms.Form):
    ORDER_CHOICES = (("newest", "Newest first"), ("oldest", "Oldest first"),
                     ("priority", "Priority: high to low"), ("updated", "Recently updated"))
    q = forms.CharField(label="Search", required=False, max_length=200, strip=True,
                        widget=forms.TextInput(attrs={"placeholder": "Title or description"}))
    status = forms.ChoiceField(required=False, choices=(("", "All statuses"), *Status.choices))
    priority = forms.ChoiceField(required=False, choices=(("", "All priorities"), *Priority.choices))
    category = forms.ModelChoiceField(required=False, queryset=Category.objects.all(), empty_label="All categories")
    order = forms.ChoiceField(label="Order", required=False, choices=ORDER_CHOICES)

    def __init__(self, parameters):
        # Only accepted scalar fields enter validation. Repeated values are ambiguous.
        data = {name: parameters.get(name, "") for name in self.base_fields}
        repeated = [name for name in self.base_fields if len(parameters.getlist(name)) > 1]
        for name in repeated:
            data[name] = ""
        data["order"] = data["order"] or "newest"
        super().__init__(data)
        self.full_clean()
        for name in repeated:
            self.add_error(name, "Supply one value. This parameter was ignored.")


def add_validation_errors(form, error):
    """Excluded workflow/model fields must become helpful non-field errors."""
    if hasattr(error, "error_dict"):
        for field, errors in error.error_dict.items():
            form.add_error(field if field in form.fields else None, errors)
    else:
        form.add_error(None, error)
