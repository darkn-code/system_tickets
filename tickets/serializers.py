from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Proyecto, Status, Ticket, StatusTicket, Mensaje, Multimedia

class ProyectoSerializer(serializers.ModelSerializer):
    grupos = serializers.SerializerMethodField()

    class Meta:
        model = Proyecto
        fields = ['id', 'nombre', 'grupos', 'created_at', 'updated_at']

    def get_grupos(self, obj):
        return list(obj.grupos.values('id', 'name'))

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensaje
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    mensajes = MensajeSerializer(many=True, read_only=True)  
    nuevo_mensaje = serializers.CharField(write_only=True, required=False,style={'base_template': 'textarea.html'}) 

    proyecto_nombre = serializers.CharField(source="proyecto.nombre", read_only=True)
    grupo_nombre = serializers.CharField(source="grupo.name", read_only=True)
    auth_user_nombre = serializers.CharField(source="auth_user.username", read_only=True)
    auth_user_atendiendo_nombre = serializers.CharField(source="auth_user_atendiendo.username", read_only=True)

    status_ticket_id = serializers.SerializerMethodField()
    status_ticket_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ["id", "asunto", "prioridad", "visible",
            "auth_user", "auth_user_nombre",
            "auth_user_atendiendo", "auth_user_atendiendo_nombre",
            "proyecto", "proyecto_nombre",
            "grupo", "grupo_nombre",
            "created_at", "updated_at",
            "mensajes", "nuevo_mensaje",
            "status_ticket_id", "status_ticket_nombre"]
        
    def get_status_ticket_id(self, ticket):
        """ Obtener el ID del último estado asignado al ticket """
        status_ticket = StatusTicket.objects.filter(ticket=ticket.id).order_by('-created_at').first()
        return status_ticket.id if status_ticket else None  

    def get_status_ticket_nombre(self, ticket):
        """ Obtener el nombre del último estado asignado al ticket """
        status_ticket = StatusTicket.objects.filter(ticket=ticket.id).order_by('-created_at').first()
        return status_ticket.status.nombre if status_ticket else None  
        
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

        if nuevo_mensaje:
            Mensaje.objects.create(
                ticket=ticket,
                auth_user=ticket.auth_user, 
                contenido=nuevo_mensaje,
                visible=True
            )
        
        status = Status.objects.filter(id=1).first()
        status_ticket = None
        if status:
            status_ticket = StatusTicket.objects.create(ticket=ticket, status=status)

        ticket.status_ticket_id = status_ticket.id if status_ticket else None
        ticket.status_ticket_nombre = status.nombre if status else None
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
    proyectos = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'proyectos']

    def get_proyectos(self, user):
        proyectos = Proyecto.objects.filter(grupos__in=user.groups.all()).distinct()
        resultado = []

        for proyecto in proyectos:
            grupos_usuario = proyecto.grupos.filter(user=user).values("id", "name")
            resultado.append({
                "id": proyecto.id,
                "nombre": proyecto.nombre,
                "grupos": list(grupos_usuario)
            })

        return resultado

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
