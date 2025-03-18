from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth.models import User, Group
from .models import Proyecto, Status, Ticket, StatusTicket, Mensaje, Multimedia
from .serializers import ProyectoSerializer, StatusSerializer, TicketSerializer, StatusTicketSerializer, MensajeSerializer, MultimediaSerializer,  UserSerializer, GroupSerializer

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