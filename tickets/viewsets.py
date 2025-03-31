from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import ProyectoSerializer
from .models import Proyecto
from rest_framework_simplejwt.authentication import JWTAuthentication

class ProyectosViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProyectoSerializer   
    queryset = Proyecto.objects.all()