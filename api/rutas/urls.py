from django.urls import path
from . import views

urlpatterns = [

    path("salida-rutas/", views.salida_ruta_list),
    path("crear-salida-ruta/", views.crear_salida_ruta),
    path("salida-rutas/<str:pk>/", views.salida_ruta_detail),
    path("venta-salida-ruta/<str:pk>/", views.venta_salida_ruta),
    path("borrar-salida-ruta/<str:pk>/", views.borrar_salida_ruta),
   
]