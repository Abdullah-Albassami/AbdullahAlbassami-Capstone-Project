"""Explicit user-editable fields; workflow metadata is supplied by services."""

from django import forms

from .models import Ticket
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


def add_validation_errors(form, error):
    """Excluded workflow/model fields must become helpful non-field errors."""
    if hasattr(error, "error_dict"):
        for field, errors in error.error_dict.items():
            form.add_error(field if field in form.fields else None, errors)
    else:
        form.add_error(None, error)
