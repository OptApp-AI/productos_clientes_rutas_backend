from rest_framework import serializers

from .models import Cliente, PrecioCliente, Ruta



class PrecioClienteSerializer(serializers.ModelSerializer): 

    # Accedemos a un atributo del padre mediante source
    producto_nombre = serializers.CharField(source='PRODUCTO.NOMBRE', read_only=True)

    # Accedemos a un atributo del padre mediante source
    producto_cantidad = serializers.IntegerField(source='PRODUCTO.CANTIDAD', read_only=True)

    class Meta:
        model = PrecioCliente
        fields = "__all__"


class ClienteSerializer(serializers.ModelSerializer):

    # Accedemos a un atributo del padre mediante source
    ruta_nombre = serializers.CharField(source="RUTA.NOMBRE", read_only=True)

    # Accedemos a los hijos mediante su serializador. Esto se conoce como serializadores anidados
    precios_cliente = PrecioClienteSerializer(many=True, read_only=True)

    class Meta:

        model = Cliente
        fields = '__all__'
        


class RutaSerializer(serializers.ModelSerializer):

    # Accedemos a un atributo especifico del hijo mediante un metodo
    cliente_id = serializers.SerializerMethodField()

    class Meta:
        model = Ruta
        fields = "__all__"


    def get_cliente_id(self, obj):
        ruta_clientes = obj.ruta_clientes.all()
        return [ruta_cliente.id for ruta_cliente in ruta_clientes]
    
    def validate(self, data):
        # Validar si ya existe un objeto con la misma combinación de NOMBRE y DIA
        ruta_existente = Ruta.objects.filter(NOMBRE=data.get('NOMBRE'), DIA=data.get('DIA')).first()
        if ruta_existente:
            raise serializers.ValidationError('Ya existe una ruta con el mismo nombre y día.')
        return data

    
   