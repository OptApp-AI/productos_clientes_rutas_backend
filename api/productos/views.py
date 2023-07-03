from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status 

from .models import Producto
from .serializers import ProductoSerializer

@api_view(['GET'])
def producto_list(request):

    # Pedir los productos de la base de datos
    queryset = Producto.objects.all()

    # Serializar productos 
    serializer = ProductoSerializer(queryset, many=True)

    # Regresar datos serializados 
    return Response(serializer.data)


@api_view(['POST'])
def crear_producto(request):

    # Serializar datos del frontend
    serializer = ProductoSerializer(data=request.data)

    # Validar datos
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET'])
def producto_detail(request, pk):

    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductoSerializer(producto)

    return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
def modificar_producto(request, pk):

    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'DELETE':
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
