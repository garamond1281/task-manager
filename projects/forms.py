from django import forms

from projects.models import Project


class ProjectSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"})
    )


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"