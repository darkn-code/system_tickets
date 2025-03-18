from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth.models import User, Group
from .models import Proyecto, Status, Ticket, StatusTicket, Mensaje, Multimedia
from .serializers import ProyectoSerializer, StatusSerializer, TicketSerializer, StatusTicketSerializer, MensajeSerializer, MultimediaSerializer,  UserSerializer, GroupSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

class ListProyectoView(ListAPIView, CreateAPIView):
    allowed_methods = ['GET', 'POST']
    serializer_class = ProyectoSerializer
    queryset = Proyecto.objects.all()

class DetailProyectoView(RetrieveUpdateDestroyAPIView):
    allowed_methods = ['GET', 'PUT', 'DELETE']
    serializer_class = ProyectoSerializer
    queryset = Proyecto.objects.all()

class ListStatusView(ListAPIView, CreateAPIView):
    allowed_methods = ['GET', 'POST']
    serializer_class = StatusSerializer
    queryset = Status.objects.all()

class DetailStatusView(RetrieveUpdateDestroyAPIView):
    allowed_methods = ['GET', 'PUT', 'DELETE']
    serializer_class = StatusSerializer
    queryset = Status.objects.all()

class ListTicketView(ListAPIView, CreateAPIView):
    allowed_methods = ['GET', 'POST']
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

class DetailTicketView(RetrieveUpdateDestroyAPIView):
    allowed_methods = ['GET', 'PUT', 'DELETE']
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

class ListStatusTicketView(ListAPIView, CreateAPIView):
    allowed_methods = ['GET', 'POST']
    serializer_class = StatusTicketSerializer
    queryset = StatusTicket.objects.all()

class DetailStatusTicketView(RetrieveUpdateDestroyAPIView):
    allowed_methods = ['GET', 'PUT', 'DELETE']
    serializer_class = StatusTicketSerializer
    queryset = StatusTicket.objects.all()

class ListMensajeView(ListAPIView, CreateAPIView):
    allowed_methods = ['GET', 'POST']
    serializer_class = MensajeSerializer
    queryset = Mensaje.objects.all()

class DetailMensajeView(RetrieveUpdateDestroyAPIView):
    allowed_methods = ['GET', 'PUT', 'DELETE']
    serializer_class = MensajeSerializer
    queryset = Mensaje.objects.all()

class ListMultimediaView(ListAPIView, CreateAPIView):
    allowed_methods = ['GET', 'POST']
    serializer_class = MultimediaSerializer
    queryset = Multimedia.objects.all()

class DetailMultimediaView(RetrieveUpdateDestroyAPIView):
    allowed_methods = ['GET', 'PUT', 'DELETE']
    serializer_class = MultimediaSerializer
    queryset = Multimedia.objects.all()


class ListUserView(ListAPIView, CreateAPIView):
    allowed_methods = ['GET', 'POST']
    serializer_class = UserSerializer
    queryset = User.objects.all()

class DetailUserView(RetrieveUpdateDestroyAPIView):
    allowed_methods = ['GET', 'PUT', 'DELETE']
    serializer_class = UserSerializer
    queryset = User.objects.all()

class ListGroupView(ListAPIView, CreateAPIView):
    allowed_methods = ['GET', 'POST']
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

class DetailGroupView(RetrieveUpdateDestroyAPIView):
    allowed_methods = ['GET', 'PUT', 'DELETE']
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class LoginView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = []  # Permitir acceso sin autenticación previa

    def get_queryset(self):
        username = self.request.query_params.get("username")
        password = self.request.query_params.get("password")

        if not username or not password:
            return User.objects.none()  # No devuelve nada si faltan credenciales

        user = authenticate(username=username, password=password)
        if user:
            return User.objects.filter(id=user.id)  # Devuelve solo el usuario autenticado

        return User.objects.none()  # Si las credenciales son incorrectas

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

        user = queryset.first()
        groups = user.groups.values_list("name", flat=True)
        proyectos = Proyecto.objects.filter(id__in=user.groups.values_list("customgroup__proyecto", flat=True)).values_list("nombre", flat=True)

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "groups": list(groups),
            "proyectos": list(proyectos),
        }, status=status.HTTP_200_OK)