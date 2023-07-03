from django.contrib import admin
from api.productos.models import Producto
from api.rutas.models import Ruta, SalidaRuta, ProductoSalidaRuta, ClienteSalidaRuta,DevolucionSalidaRuta
from api.clientes.models import Cliente, PrecioCliente
# Register your models here.

admin.site.register(Producto)
admin.site.register(Ruta)
admin.site.register(SalidaRuta)
admin.site.register(ProductoSalidaRuta)
admin.site.register(ClienteSalidaRuta)
admin.site.register(DevolucionSalidaRuta)
admin.site.register(Cliente)
admin.site.register(PrecioCliente)