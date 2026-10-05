from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from workers.models import Position, Worker


class WorkerSearchForm(forms.Form):
    first_name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"})
    )
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=False,
        empty_label="All positions",
        label=""
    )

class WorkerCreationForm(UserCreationForm):
    class Meta:
        user = get_user_model()
        model = user
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "position"
        )


class BootstrapFormMixin:
    """Adds Bootstrap's form-control class to every widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{css_class} form-control".strip()


class UserRegisterForm(BootstrapFormMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + ("email",)