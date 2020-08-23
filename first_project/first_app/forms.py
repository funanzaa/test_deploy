from django import forms
from django.core import validators
from first_app.models import User


def check_for_z(value):
    if value[0].lower() != 'z':
        raise forms.ValidationError("Name Need To Start With Z")

class FormName(forms.Form):
    name = forms.CharField(validators=[check_for_z])
    email = forms.EmailField()
    verify_email = forms.EmailField(label='Enter your email again ')
    text = forms.CharField(widget=forms.Textarea)

    def clean(self):
        all_clean_data = super().clean()
        email = all_clean_data['email']
        vmail = all_clean_data['verify_email']

        if email != vmail:
            raise forms.ValidationError("Make Sure Emails Match!")
    # botchtcher = forms.CharField(required=False, widget=forms.HiddenInput, validators= [validators.MaxLengthValidator(0)] )

    # def clean_botchtcher(self):
    #     botchtcher = self.cleaned_data['botchtcher']
    #     if len(botchtcher) > 0:
    #         raise forms.ValidationError("Gotcha bot!")
    #     return botchtcher

class NewUserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = '__all__'
