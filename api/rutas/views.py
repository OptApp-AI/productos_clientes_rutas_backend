from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import SalidaRuta, ProductoSalidaRuta, ClienteSalidaRuta
from api.productos.models import Producto
from api.clientes.models import Cliente
from .serializers import SalidaRutaSerializer, ProductoSalidaRutaSerializer, ClienteSalidaRutaSerializer
from django.db.models import Q

@api_view(['GET'])
def salida_ruta_list(request):

    queryset = SalidaRuta.objects.all()

    serializer = SalidaRutaSerializer(queryset, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def salida_ruta_detail(request, pk):

    try:
        salida_ruta = SalidaRuta.objects.get(pk=pk)
    except SalidaRuta.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

    serializer = SalidaRutaSerializer(salida_ruta)

    return Response(serializer.data)

@api_view(['POST'])
def crear_salida_ruta(request):

    data = request.data 

    serializer = SalidaRutaSerializer(data=data)

    if serializer.is_valid():
        salida_ruta = serializer.save()

        # Generar ProductoSalidaRuta 
        salida_ruta_productos = data['salidaRutaProductos']

        for salida_ruta_producto in salida_ruta_productos:

            producto = Producto.objects.get(pk=salida_ruta_producto["productoId"])

            producto_salida_ruta = ProductoSalidaRuta.objects.create(
                SALIDA_RUTA = salida_ruta, 
                PRODUCTO_RUTA = producto,
                CANTIDAD_RUTA = salida_ruta_producto["cantidadSalidaRuta"],
                CANTIDAD_DISPONIBLE = salida_ruta_producto["cantidadSalidaRuta"],
                STATUS = "CARGADO"
            )

            producto.CANTIDAD -= producto_salida_ruta.CANTIDAD_RUTA
            producto.save()
            producto_salida_ruta.save()
  
        
        # Genrar ClienteSalidaRuta 
        salida_ruta_clientes = data['salidaRutaClientes']

        for salida_ruta_cliente in salida_ruta_clientes:

            cliente_salida_ruta = ClienteSalidaRuta.objects.create(
                SALIDA_RUTA = salida_ruta,
                CLIENTE_RUTA = Cliente.objects.get(id = salida_ruta_cliente["clienteId"]),
                STATUS = "PENDIENTE"
            )

            cliente_salida_ruta.save()
        
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def venta_salida_ruta(request, pk):
    
    data = request.data 

    # Actualizar productos salida ruta 
    productos_venta = data['productosVenta']

    for producto_venta in productos_venta:

        producto_salida_ruta = ProductoSalidaRuta.objects.get(pk=producto_venta["productoId"])

        producto_salida_ruta.CANTIDAD_DISPONIBLE -= producto_venta["cantidadVenta"]

        if producto_salida_ruta.CANTIDAD_DISPONIBLE == 0:
            producto_salida_ruta.STATUS = "VENDIDO"
        
        producto_salida_ruta.save()
    
    # Actualizar cliente salida ruta 
    cliente_salida_ruta = ClienteSalidaRuta.objects.get(id = data['clienteId'])

    cliente_salida_ruta.STATUS = "VISITADO"

    cliente_salida_ruta.save()

    # Obtener salida ruta
    salida_ruta = SalidaRuta.objects.get(id = pk)

    # Obtener todos los productos salida ruta 
    salida_ruta_productos = salida_ruta.salida_ruta_productos.all()
    # Obtener todos los clientes salida ruta
    salida_ruta_clientes = salida_ruta.salida_ruta_clientes.all()

    nuevo_status_salida_ruta = obtener_nuevo_status(salida_ruta_productos, salida_ruta_clientes)

    salida_ruta.STATUS = nuevo_status_salida_ruta

    salida_ruta.save()

    serializer = SalidaRutaSerializer(salida_ruta)

    return Response(serializer.data)

    
    
def obtener_nuevo_status(salida_ruta_productos, salida_ruta_clientes):

    if salida_ruta_productos.filter(~Q(STATUS="VENDIDO")).exists() or  salida_ruta_clientes.filter(~Q(STATUS="VISITADO")).exists():
        return "PROGRESO"
    return "REALIZADO"



@api_view(['DELETE'])
def borrar_salida_ruta(request, pk):
    
    try:
        salida_ruta = SalidaRuta.objects.get(pk=pk)
        
    except SalidaRuta.DoesNotExist:
        return Response({"Detalles":"No se encontró la salida ruta"},status=status.HTTP_404_NOT_FOUND)


    reporte_cambios = {}


    try:
        status_actual = salida_ruta.STATUS
        assert status_actual == "PENDIENTE"
    except AssertionError:
        return Response({"Detalles:", "El STATUS actual debe ser PENDIENTE para poder cancelar la salida ruta"}, status=status.HTTP_400_BAD_REQUEST)
    
    status_cambios = {"ANTES": status_actual}

    salida_ruta_productos = salida_ruta.salida_ruta_productos 

    salida_ruta_productos_serializer = ProductoSalidaRutaSerializer(salida_ruta_productos, many=True)
    
    for salida_ruta_producto_serializer in salida_ruta_productos_serializer.data:

        producto = Producto.objects.get(NOMBRE = salida_ruta_producto_serializer["producto_nombre"])
        
        producto_cambios= {"ANTES": producto.CANTIDAD}

        cantidad_salida_ruta = salida_ruta_producto_serializer["CANTIDAD_RUTA"]

        producto.CANTIDAD += cantidad_salida_ruta

        producto.save()

        producto_cambios["DESPUES"] = producto.CANTIDAD

        reporte_cambios[producto.NOMBRE] = producto_cambios
    

    salida_ruta.delete()
    status_cambios["DESPUES"] = "CANCELADO"
    reporte_cambios["STATUS"] = status_cambios

    return Response(reporte_cambios)


    