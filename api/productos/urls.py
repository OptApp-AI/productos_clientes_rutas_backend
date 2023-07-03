from django.urls import path
from . import views

urlpatterns = [
    path("productos/", views.producto_list),
    path("crear-producto/", views.crear_producto),
    path("productos/<str:pk>/", views.producto_detail), 
    path("modificar-producto/<str:pk>/", views.modificar_producto),
]