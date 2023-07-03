from rest_framework import serializers
from .models import SalidaRuta, ProductoSalidaRuta, ClienteSalidaRuta
from api.clientes.models import PrecioCliente
from api.clientes.serializers import PrecioClienteSerializer


class ProductoSalidaRutaSerializer(serializers.ModelSerializer):

    # Accedemos a un atributo del padre mediante source
    producto_nombre = serializers.CharField(source='PRODUCTO_RUTA.NOMBRE', read_only=True)

    class Meta: 
        model = ProductoSalidaRuta
        fields = ("id", "producto_nombre", "CANTIDAD_RUTA", "CANTIDAD_DISPONIBLE", "STATUS")
        # fields = '__all__'

class ClienteSalidaRutaSerializer(serializers.ModelSerializer):

    # Accedemos a un atributo del padre mediante source
    nombre = serializers.CharField(source="CLIENTE_RUTA.NOMBRE", read_only=True)
    # Accedemos a los atributos especificos de un hermano mediante un metodo
    precios_cliente = serializers.SerializerMethodField()
    

    class Meta:
        model = ClienteSalidaRuta
        fields = ("id", "nombre", "STATUS", "precios_cliente")
        # fields = "__all__"    
    
    # Asi accedo a los atributos de un hermano desde el serializador
    def get_precios_cliente(self, obj):
        precios_cliente = []
        # PrecioCliente es hermano de ClienteSalida porque los dos son hijos de Cliente

        # Dame todos las instancias de PRecioCliente que son hijas de mi papa (Cliente)
        for precio in PrecioCliente.objects.filter(CLIENTE=obj.CLIENTE_RUTA):
            # Serializa a mi hermano
            serializer = PrecioClienteSerializer(precio)
            # Usa la informacion en mi hermano serializado para crear un objeto y agregarlo a precios_cliente
            precios_cliente.append({
                "precio": serializer.data["PRECIO"], 
                "producto_nombre": serializer.data["producto_nombre"], 
                # "productoId": serializer.data['PRODUCTO'],
            })
            # precios_cliente.append(serializer.data)
        return precios_cliente
   


class SalidaRutaSerializer(serializers.ModelSerializer):

    salida_ruta_productos = ProductoSalidaRutaSerializer(many=True, read_only=True)

    salida_ruta_clientes = ClienteSalidaRutaSerializer(many=True, read_only=True)



    class Meta:
        model = SalidaRuta
        fields = '__all__'







    