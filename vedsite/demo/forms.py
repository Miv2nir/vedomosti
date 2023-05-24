from django import forms


class AuthForm(forms.Form):
    login = forms.CharField(label='Login', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100, widget=forms.EmailInput)
    login = forms.CharField(label='Login', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
    password_verify = forms.CharField(label='Repeat Password', max_length=100, widget=forms.PasswordInput)


class LogOutForm(forms.Form):
    logout = forms.CharField()


class CredentialsForm(forms.Form):
    ya_login = forms.CharField(label='Yandex.Contest Login', max_length=100)
    ya_password = forms.CharField(label='Yandex.Contest Password', max_length=100, widget=forms.PasswordInput)
    ya_id = forms.IntegerField(label='Yandex.Contest Contest ID')


class DisciplineForm(forms.Form):
    d_name = forms.CharField(widget=forms.TextInput(attrs={"class": "square_input"}))

# class DisciplineForm(forms.Form):
