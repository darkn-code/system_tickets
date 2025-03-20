from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Proyecto, Status, Ticket, StatusTicket, Mensaje, Multimedia

class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensaje
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    mensajes = MensajeSerializer(many=True, read_only=True)  # Mostrar mensajes existentes en un ticket
    nuevo_mensaje = serializers.CharField(write_only=True, required=False,style={'base_template': 'textarea.html'})  # Permitir crear un mensaje al crear ticket

    class Meta:
        model = Ticket
        fields = ["id", "asunto", "prioridad", "visible", "auth_user_atendiendo",
                  "auth_user", "proyecto", "grupo", "created_at", "updated_at", "mensajes", "nuevo_mensaje"]
        
    def validate(self, data):
        """ Validar que el grupo pertenece al proyecto seleccionado """
        proyecto = data.get("proyecto")
        grupo = data.get("grupo")

        if proyecto and grupo:
            if grupo not in proyecto.grupos.all():
                raise serializers.ValidationError("El grupo seleccionado no pertenece a este proyecto.")

        return data

    def create(self, validated_data):
        nuevo_mensaje = validated_data.pop("nuevo_mensaje", None)  # Extraer el mensaje si existe
        ticket = Ticket.objects.create(**validated_data)

        # Si se envió un mensaje, crearlo asociado al Ticket
        if nuevo_mensaje:
            Mensaje.objects.create(
                ticket=ticket,
                auth_user=ticket.auth_user,  # El usuario que creó el ticket es el autor del mensaje
                contenido=nuevo_mensaje,
                visible=True
            )

        return ticket

class StatusTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusTicket
        fields = '__all__'

class MultimediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Multimedia
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
