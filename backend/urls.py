from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.productos.urls')),
    path('api/', include('api.clientes.urls')),
    path('api/', include('api.rutas.urls')),
    path('api/', include('api.usuarios.urls')),
]
