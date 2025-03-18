from django.db import models
from django.contrib.auth.models import User, Group

class Proyecto(models.Model):
    nombre = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Status(models.Model):
    nombre = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Ticket(models.Model):
    asunto = models.CharField(max_length=255)
    prioridad = models.IntegerField()
    visible = models.BooleanField(default=True)
    auth_user_atendiendo = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tickets_atendidos')
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets_creados')
    auth_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class StatusTicket(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    comentarios = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Mensaje(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
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