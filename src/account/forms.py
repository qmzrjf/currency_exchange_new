from django.forms import ModelForm
from account.models import User
from django import forms


class SignUpForm(ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'phone')

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            if cleaned_data['password'] != cleaned_data['password2']:
                raise forms.ValidationError('Password do not match! ')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = False
        user.save()

        sms_code = user.activation_code_sms.create()
        sms_code.send_activation_sms_code()
        return user


class ActivateForm(forms.Form):
    sms_code = forms.CharField()