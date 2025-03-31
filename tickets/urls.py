from django.urls import path
from .views import (
    ListProyectoView, DetailProyectoView,
    ListStatusView, DetailStatusView,
    ListTicketView, DetailTicketView,
    ListStatusTicketView, DetailStatusTicketView,
    ListMensajeView, DetailMensajeView,
    ListMultimediaView, DetailMultimediaView,
    ListUserView, DetailUserView,
    ListGroupView, DetailGroupView,
    LoginView, ListicketUserView, SearchTicketView,CustomTokenObtainPairView
)
from rest_framework.routers import DefaultRouter
from .viewsets import ProyectosViewSet

from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt import views as jwt_views

router = DefaultRouter()
router.register('proyectos',ProyectosViewSet)

urlpatterns = [
    #path('proyectos/', ListProyectoView.as_view(), name='list_proyectos'),
    #path('proyectos/<int:pk>/', DetailProyectoView.as_view(), name='detail_proyecto'),
    
    path('statuses/', ListStatusView.as_view(), name='list_statuses'),
    path('statuses/<int:pk>/', DetailStatusView.as_view(), name='detail_status'),
    
    path('tickets/', ListTicketView.as_view(), name='list_tickets'),
    path('tickets/<int:pk>/', DetailTicketView.as_view(), name='detail_ticket'),
    
    path('status_tickets/', ListStatusTicketView.as_view(), name='list_status_tickets'),
    path('status_tickets/<int:pk>/', DetailStatusTicketView.as_view(), name='detail_status_ticket'),
    
    path('mensajes/', ListMensajeView.as_view(), name='list_mensajes'),
    path('mensajes/<int:pk>/', DetailMensajeView.as_view(), name='detail_mensaje'),
    
    path('multimedia/', ListMultimediaView.as_view(), name='list_multimedia'),
    path('multimedia/<int:pk>/', DetailMultimediaView.as_view(), name='detail_multimedia'),

     path('usuarios/', ListUserView.as_view(), name='list_usuarios'),
    path('usuarios/<int:pk>/', DetailUserView.as_view(), name='detail_usuario'),
    
    path('grupos/', ListGroupView.as_view(), name='list_grupos'),
    path('grupos/<int:pk>/', DetailGroupView.as_view(), name='detail_grupo'),

    path("login/", LoginView.as_view(), name="login"),

    path('ticketsUser/<int:pk>/', ListicketUserView.as_view(), name='ticket-user'),
    path('ticketsSearch/', SearchTicketView.as_view(), name='search_tickets'),

    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtener el token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # Renovar el token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

] + router.urls
