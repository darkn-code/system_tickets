from .forms import CreateUserForm, LoginUserForm
from django.views import generic
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class RegisterView(generic.CreateView):
    form_class = CreateUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')


class LoginDarkView(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'



