from django.urls import path
from .views import (
    ListProyectoView, DetailProyectoView,
    ListStatusView, DetailStatusView,
    ListTicketView, DetailTicketView,
    ListStatusTicketView, DetailStatusTicketView,
    ListMensajeView, DetailMensajeView,
    ListMultimediaView, DetailMultimediaView
)

urlpatterns = [
    path('proyectos/', ListProyectoView.as_view(), name='list_proyectos'),
    path('proyectos/<int:pk>/', DetailProyectoView.as_view(), name='detail_proyecto'),
    
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
]
