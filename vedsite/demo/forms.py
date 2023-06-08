from django import forms


class AuthForm(forms.Form):
    # login = forms.CharField(label='Login', max_length=100)
    login = forms.CharField(label='Login', widget=forms.TextInput(attrs={'placeholder': 'Login', 'class': 'square_login'}))

    # password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'square_login'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""


class RegisterForm(forms.Form):
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'square_login'}))
    login = forms.CharField(label='Login', widget=forms.TextInput(attrs={'placeholder': 'Login', 'class': 'square_login'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'square_login'}))
    password_verify = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password', 'class': 'square_login'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""


class NewAuthForm(forms.Form):
    password_old = forms.CharField(label='Old Password', max_length=100, widget=forms.PasswordInput)
    password = forms.CharField(label='New Password', max_length=100, widget=forms.PasswordInput)
    password_verify = forms.CharField(label='Repeat Password', max_length=100, widget=forms.PasswordInput)


class LogOutForm(forms.Form):
    logout = forms.CharField()


class CredentialsForm(forms.Form):
    ya_login = forms.CharField(label='Yandex.Contest Login', widget=forms.TextInput(attrs={'placeholder': 'Ya.Contest Login', 'class': 'square_login'}))
    ya_password = forms.CharField(label='Yandex.Contest Password', widget=forms.PasswordInput(attrs={'placeholder': 'Ya.Contest Password', 'class': 'square_login'}))
    ya_id = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Contest ID', 'class': 'square_login'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""


class DisciplineForm(forms.Form):
    d_name = forms.CharField(widget=forms.TextInput(attrs={"class": "square_input"}))


class DisciplineListForm(forms.Form):
    # d_uuid = forms.UUIDField()
    def __init__(self, *args, **kwargs):
        d_names = kwargs.pop('d_names')
        super(DisciplineListForm, self).__init__(*args, **kwargs)
        for name in d_names:
            self.fields['d_og_name_'+name] = forms.CharField(widget=forms.TextInput(attrs={"class": "square_input_manage"}), initial=name)


class GroupForm(forms.Form):
    g_number = forms.IntegerField(widget=forms.TextInput(attrs={"class": "square_input"}))


class GroupListForm(forms.Form):
    # d_uuid = forms.UUIDField()
    def __init__(self, *args, **kwargs):
        g_numbers = kwargs.pop('g_numbers')
        super(GroupListForm, self).__init__(*args, **kwargs)
        for number in g_numbers:
            self.fields['g_og_number_'+str(number)] = forms.CharField(widget=forms.TextInput(attrs={"class": "square_input_manage"}), initial=number)
# class DisciplineForm(forms.Form):
