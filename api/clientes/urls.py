from django.urls import path
from . import views

urlpatterns = [
    path("clientes/", views.cliente_list),
    path("crear-cliente/", views.crear_cliente),
    path("clientes/<str:pk>/", views.cliente_detail),
    path("modificar-cliente/<str:pk>/", views.modificar_cliente),
    path("rutas/", views.ruta_list),
    path("rutas/<str:pk>/", views.ruta_detail),
    path("crear-ruta/", views.crear_ruta),
    path("modificar-ruta/<str:pk>/", views.modificar_ruta),
]
