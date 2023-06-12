from django import forms
from .models import Student


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


class NewPasswordForm(forms.Form):
    password_old = forms.CharField(label='Old Password', max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Old Password', 'class': 'square_login'}))
    password = forms.CharField(label='New Password', max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'square_login'}))
    password_verify = forms.CharField(label='Repeat Password', max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password', 'class': 'square_login'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""


class LogOutForm(forms.Form):
    logout = forms.CharField()


class CredentialsForm(forms.Form):
    ya_l = forms.CharField(required=False, label='Yandex.Contest1', widget=forms.TextInput(attrs={'placeholder': 'Yandex.Contest Login', 'class': 'square_login', 'autocomplete': "new-password"}))
    ya_p = forms.CharField(required=False, label='Yandex.Contest2', widget=forms.PasswordInput(attrs={'placeholder': 'Yandex.Contest Password', 'class': 'square_login', 'autocomplete': "new-password"}))

    step_id = forms.CharField(required=False, label='Stepik Client ID', widget=forms.TextInput(attrs={'placeholder': 'Stepik Client ID', 'class': 'square_login', 'autocomplete': "new-password"}))
    step_api = forms.CharField(required=False, label='Stepik Client Secret', widget=forms.PasswordInput(attrs={'placeholder': 'Stepik Client Secret', 'class': 'square_login', 'autocomplete': "new-password"}))
    # ya_id = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Contest ID', 'class': 'square_login'}))

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


class StudentForm(forms.Form):
    # s_display_name = forms.CharField(label='Login', widget=forms.TextInput(attrs={'placeholder': 'Student Display Name', 'class': 'square_login'}))
    # s_email = forms.CharField(required=False, label='Login', widget=forms.TextInput(attrs={'placeholder': 'Student Email', 'class': 'square_login'}))
    s_ya_name = forms.CharField(required=False, label='Login', widget=forms.TextInput(attrs={'placeholder': 'Ya.Contest Student Name', 'class': 'square_login'}))
    s_stepik_name = forms.CharField(required=False, label='Login', widget=forms.TextInput(attrs={'placeholder': 'Stepik Student Name', 'class': 'square_login'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""


class PlatformSelectForm(forms.Form):
    p_choice = forms.ChoiceField(widget=forms.Select(attrs={'class': 'square_login_big'}), choices=[('yandex', 'Yandex Contest'), ('stepik', 'Stepik')])
    p_id = forms.CharField(label='TID', widget=forms.TextInput(attrs={'placeholder': 'Enter Contest ID', 'class': 'square_login'}))


'''
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ["s_id", "s_owner", "d_id", "g_number"]

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['s_ya_name'].widget.attrs.update({'placeholder': 'Ya.Contest Student Name', 'class': 'square_login'})
        self.fields['s_stepik_name'].widget.attrs.update({'placeholder': 'Stepik Student Name', 'class': 'square_login'})
        self.fields['s_display_name'].widget.attrs.update({'placeholder': 'Student Display Name', 'class': 'square_login'})
        self.fields['s_email'].widget.attrs.update({'placeholder': 'Student Email', 'class': 'square_login'})
        for key, field in self.fields.items():
            field.label = ""
'''


class StudentListForm(forms.Form):
    def __init__(self, *args, **kwargs):
        s_numbers = kwargs.pop('s_numbers')
        super(StudentListForm, self).__init__(*args, **kwargs)
        for number in s_numbers:
            self.fields['']

# class DisciplineForm(forms.Form):
