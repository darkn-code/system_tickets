from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Proyecto, Status, Ticket, StatusTicket, Mensaje, Multimedia, UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
    auth_user_nombre = serializers.CharField(source='auth_user.username', read_only=True)
    class Meta:
        model = Mensaje
        fields = ['id', 'contenido', 'visible', 'created_at','ticket', 'auth_user_nombre']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['auth_user'] = request.user
        return Mensaje.objects.create(**validated_data)

class TicketSerializer(serializers.ModelSerializer):
    mensaje_count = serializers.SerializerMethodField() 
    nuevo_mensaje = serializers.CharField(write_only=True, required=False,style={'base_template': 'textarea.html'}) 

    proyecto_nombre = serializers.CharField(source="proyecto.nombre", read_only=True)
    grupo_nombre = serializers.CharField(source="grupo.name", read_only=True)
    auth_user_nombre = serializers.CharField(source="auth_user.username", read_only=True)
    auth_user_atendiendo_nombre = serializers.CharField(source="auth_user_atendiendo.username", read_only=True)

    status_ticket_id = serializers.SerializerMethodField()
    status_ticket_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ["id", "asunto", "prioridad","auth_user_atendiendo",
             "auth_user_nombre","auth_user_atendiendo_nombre",
            "proyecto", "proyecto_nombre",
            "grupo", "grupo_nombre",
            "created_at","mensaje_count", "nuevo_mensaje",
            "status_ticket_id", "status_ticket_nombre"]
        
        
    def get_mensaje_count(self, ticket):
        """ 🔹 Obtener la cantidad de mensajes asociados al ticket """
        return ticket.mensajes.count()

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
        request = self.context.get('request')
        nuevo_mensaje = validated_data.pop("nuevo_mensaje", None)  # Extraer el mensaje si existe
        validated_data['auth_user'] = request.user
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


class TicketiDSerializer(serializers.ModelSerializer):
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
        fields = ["id", "asunto", "prioridad",
            "auth_user_nombre","auth_user_atendiendo_nombre",
            "proyecto", "proyecto_nombre",
            "grupo", "grupo_nombre",
            "created_at","mensajes", "nuevo_mensaje",
            "status_ticket_id", "status_ticket_nombre"]
        read_only_fields = ['auth_user_nombre', 'auth_user_atendiendo_nombre', 'mensajes', 'created_at']
        
        
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
        request = self.context.get('request')
        nuevo_mensaje = validated_data.pop("nuevo_mensaje", None)  # Extraer el mensaje si existe
        validated_data['auth_user'] = request.user
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
    rol = serializers.IntegerField(write_only=True) 
    rol_display = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=True) 
    class Meta:
        model = User
        fields = ['id', 'username','password', 'email', 'first_name', 'last_name', 'rol','rol_display', 'proyectos']

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
    
    def get_rol(self, user):
        """ Obtener el rol desde UserProfile """
        return getattr(UserProfile.objects.filter(user=user).first(), 'rol', 0) 
    
    def get_rol_display(self, user):
        return getattr(UserProfile.objects.filter(user=user).first(), 'rol', 0) 
    
    def create(self, validated_data):
        rol = validated_data.pop('rol', None) 
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        
        if password:
            user.set_password(password)
        else:
            user.set_password('defaultpassword123')  # Contraseña por defecto

        user.save()

        user.userprofile.rol = rol if rol is not None else 3  
        user.userprofile.save()

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        rol = validated_data.pop('rol', 5) 
        if password:
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if rol is not None:
            profile, created = UserProfile.objects.get_or_create(user=instance)
            profile.rol = rol
            profile.save()

        return instance

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user  # Usuario autenticado

        # Datos del usuario
        data['user_id'] = user.id
        data['username'] = user.username
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['email'] = user.email
        user_profile = UserProfile.objects.get(user=user)  # Obtener el perfil del usuario
        data['rol'] = user_profile.rol 

        # Obtener los proyectos del usuario con sus grupos
        proyectos = Proyecto.objects.filter(grupos__in=user.groups.all()).distinct()
        proyectos_data = []
        for proyecto in proyectos:
            grupos_usuario = proyecto.grupos.filter(user=user).values("id", "name")
            proyectos_data.append({
                "id": proyecto.id,
                "nombre": proyecto.nombre,
                "grupos": list(grupos_usuario)  # Lista de grupos con id y nombre
            })

        data['proyectos'] = proyectos_data  # Agregar proyectos al JSON de respuesta

        return data


