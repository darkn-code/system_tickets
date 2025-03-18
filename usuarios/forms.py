from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from crispy_forms.bootstrap import FieldWithButtons, StrictButton

class LoginUserForm(AuthenticationForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Div(
            Div('username', css_class='col-12'),
            Div(FieldWithButtons('password', StrictButton('<i class="bi bi-eye"></i>', type='button', css_class='btn btn-outline-secondary', id='password1Button')), css_class='col-6'
                ),
            css_class='row'
        )
    )

    username = forms.CharField(
         label = 'Usuario',
         required=True,
     )
    
    password = forms.CharField(
         label = "Contraseña",
         widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
         required=True
     )
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

class CreateUserForm(UserCreationForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Div(
            Div('username', css_class='col-12'),
            Div(FieldWithButtons('password1', StrictButton('<i class="bi bi-eye"></i>', type='button', css_class='btn btn-outline-secondary', id='password1Button')), css_class='col-6'
                ),
            Div(FieldWithButtons('password2', StrictButton('<i class="bi bi-eye"></i>', type='button', css_class='btn btn-outline-secondary', id='password2Button')), css_class='col-6'
                ),
            css_class='row'
        )
    )

    username = forms.CharField(
         label = 'Usuario',
         required=True,
     )
    password1 = forms.CharField(
         label = "Contraseña",
         required=True
     )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2']

