from .forms import CreateUserForm, LoginUserForm
from django.views import generic
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
import requests
from rest_framework import status


class RegisterView(generic.CreateView):
    form_class = CreateUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')


class LoginDarkView(LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        """Cuando el login es exitoso, genera un token JWT y lo guarda en una cookie."""
        response = super().form_valid(form)  # Llamamos al método original para autenticar

        # Obtener el usuario autenticado
        user = form.get_user()
        refresh = RefreshToken.for_user(user)  # Generar JWT
        access_token = str(refresh.access_token)
        print(access_token)
        # Guardar token en cookies
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,  # No accesible desde JavaScript
            secure=False,   # Cambia a True en producción con HTTPS
            samesite="Lax",
        )

        # Redirigir a /api/proyectos/
        return HttpResponseRedirect(reverse_lazy('proyecto-list'))  

    def form_invalid(self, form):
        """Si el login falla, devuelve un error JSON."""
        return JsonResponse({"error": "Credenciales inválidas"}, status=400)