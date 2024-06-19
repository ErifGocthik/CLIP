from django import forms

from cloudapp.models import Archive


class ArchiveCreateForm(forms.ModelForm):
    class Meta:
        model = Archive
        fields = ['name']