from django import forms


class SignupForm(forms.Form):
    email = forms.EmailField(label='An email to log in with')

    username = forms.EmailField(label='A username (to be displayed on comments and other submissions)')

    password = forms.CharField(widget=forms.PasswordInput())
    password_duplicate = forms.CharField(widget=forms.PasswordInput(), label='Confirm password')