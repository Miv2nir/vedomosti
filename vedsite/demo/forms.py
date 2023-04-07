from django import forms


class AuthForm(forms.Form):
    login = forms.CharField(label='login', max_length=100)
    password = forms.CharField(label='password', max_length=100, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    email = forms.CharField(label='email', max_length=100, widget=forms.EmailInput)
    login = forms.CharField(label='login', max_length=100)
    password = forms.CharField(label='password', max_length=100, widget=forms.PasswordInput)
    password_verify = forms.CharField(label='password_verify', max_length=100, widget=forms.PasswordInput)


class LogOutForm(forms.Form):
    logout = forms.CharField()


class CredentialsForm(forms.Form):
    ya_login = forms.CharField(label='Yandex.Contest Login', max_length=100)
    ya_password = forms.CharField(label='Yandex.Contest Passwoed', max_length=100, widget=forms.PasswordInput)
    ya_id = forms.IntegerField(label='Yandex.Contest Contest ID')
