from django.db import models
from django.contrib.auth.models import User, Group
from django.db import models


class UserProfile(models.Model):
    ROL_CHOICES = [
        (1, 'Admin'),
        (2, 'Soporte'),
        (3, 'Usuario')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    rol = models.IntegerField(choices=ROL_CHOICES, default=3)

    def __str__(self):
        return dict(self._meta.get_field('rol').choices).get(self.rol, 'Unknown')

class Proyecto(models.Model):
    nombre = models.CharField(max_length=255)
    grupos = models.ManyToManyField(Group, related_name="proyectos")  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.id})" 

class Status(models.Model):
    nombre = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.id})" 

class Ticket(models.Model):
    asunto = models.CharField(max_length=255)
    prioridad = models.IntegerField()
    visible = models.BooleanField(default=True)
    auth_user_atendiendo = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tickets_atendidos')
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets_creados')
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.proyecto}:{self.grupo} ({self.id})" 

class StatusTicket(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    comentarios = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Mensaje(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="mensajes")
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    visible = models.BooleanField(default=True)
    is_media = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Multimedia(models.Model):
    multimedia_type = models.CharField(max_length=50)
    url = models.URLField()
    nombre = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

