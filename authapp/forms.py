from django.contrib.auth.forms import UserCreationForm


class CustomUserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form_control'})

        for field in list(self.fields.values()):
            field.widget.attrs.update({'class': 'form_control'})