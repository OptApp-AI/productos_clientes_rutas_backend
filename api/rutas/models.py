from django.db import models
from django.core.validators import MinValueValidator
from api.productos.models import Producto
from api.clientes.models import Ruta, Cliente
# Lo de la ruta es solo para facilitar cargar la lista de clientes


# Una salida a ruta es parecida a una venta:

# 1. LOS PRODUCTOS DE SALIDA A RUTA SE RETIRAN DEL STOCK SIEMPRE. NO IMPORTA EL STATUS 
# 2. EXISTEN LOS MISMOS TRES STATUS: PENDIENTE, REALIZADO, CANCELADO. SIEMPRE SE GENERA CON STATUS PENDIENTE 
# 3. EN GENERAL LOS CAMPOS SON SIMIILARES (ATIENDE, FECHA, OBSERVACIONES, ETC.)
# 4. SOLO LOS ADMINISTRADORES PUEDEN PASAR EL STATUS DE PENDIENTE A REALIZADO O CANCELADO, O DE REALIZADO A CANCELADO. PUEDEN ESCOGER CANCELAR DE FORMA DIRECTA, PERO PARA PASAR EL STATUS A REALIZADO ES A TRAVES DE DEVOLUCIONES 
# 5. SE PUEDEN HACER DEVOLUCIONES. LAS DEVOLUCIONES LAS PUEDEN HACER CAJEROS (LUEGO VEMOS A LOS ADMIS)
# 6. AL HACER ESTO SE GENERA UNA DEVOLUCION CON STATUS DE PENDIENTE. SOLO HASTA QUE EL ADMI CAMBIA SU STATUS A REALIZADO ES QUE SE REGRESAN LOS PRODUCTOS AL SOTCK
# 7. CUANDO EL CAJERO ENTRE A LA SALIDARUTA, SOLO PUEDE DEVOLVER LOS PRODUCTOS CON STATUS DE CARGADO
class SalidaRuta(models.Model):
    RUTA = models.ForeignKey(Ruta, on_delete=models.SET_NULL, null=True)
    FECHA = models.DateTimeField(auto_now=True)
    ATIENDE = models.CharField(max_length=100)
    REPARTIDOR = models.CharField(max_length=100)
    # Si hubo una devolucion en esta salida a ruta el administrador va a hacer la devolucion aqui 
    OBSERVACIONES = models.CharField(max_length=200)
    STATUS = models.CharField(max_length=100, choices=(
        # Sale como pendiente mientras no venta todos los productos. Si al final del corte hay productos y se requiere una devolucion. Es necesario hacer una devolucion para cambiar el status a realizado. O bien, se pueden cancelar. 
        ("PENDIENTE", "PENDIENTE"), 
        ("PROGRESO", "PROGRESO"), 
        # Cambia a realizado cuando vendio todos los productos
        # Cada vez que se vende un ProductoSalidaRuta de esta salida ruta se verifica esto para ver si se debe cambiar
        ("REALIZADO", "REALIZADO"), 
        # Se puede cancelar y todos los productos se regresan al almacen. Todos los ProductoSalidaRuta y ClienteSalidaRuta se cancelan.
        #  NO ES POSIBLE CANCELAR SI YA SE VENDIO ALGO
        ("CANCELADO", "CANCELADO")))

    def __str__(self):
        # DESPUES HAY QUE CAMBIAR ESTO PORQUE SI SE BORRA EL ATIENDE O REPARTIDOR VAN A EXISTIR PROBLEMAS
        return f"{self.ATIENDE}, {self.REPARTIDOR}"

# Todo lo que esta aqui abajo solo se accede, crea, borra o actualiza a traves de SalidaRuta
# Menos devoluciones.
# Esto es lo que se le carga al repartidor
# El repartidor solo puede vender ProductoSalidaRuta 
# Solo le puede vender a ClienteSalidaRuta

# De aqui se van hacia la venta o se regresan al stock mediante una devolucion/cancelacion
# La devolucion es aqui 
# ESTOY ASUMIENDO QUE LOS REPARTIDOES NO APLICAN CORTESIA NI DESCUENTO ADISIONAL



# PARA CREAR ESTA PARTE VOY A CREAR UNA INTERFAZ DE USUARIO DONDE PUEDO SELECCIONAR UN CLIENTE, SUS PRODUCTOS Y CON ESTO VOY MODIFICANDO LOS STATUS DE PRODUCTO Y CLIENTE 
# ProductoSalidaRuta cambia a vendido cuando ya me acabe todo el producto 
# ClienteSalidaRuta cambia a visitado cuando ya le vendi a todos los clientes

# El status cambia a vendido hasta que todo el producto se vendio 
class ProductoSalidaRuta(models.Model):
    # Si la salida a ruta se cancela los ProductoSalidaRuta se cancelan
    SALIDA_RUTA = models.ForeignKey(SalidaRuta, on_delete=models.CASCADE, related_name="salida_ruta_productos")
    # Aqui si usamos el objeto producto porque sera necesario acceder a este para hacer las devoluciones
    PRODUCTO_RUTA = models.ForeignKey(Producto, on_delete=models.CASCADE)
    CANTIDAD_RUTA = models.IntegerField(validators=[MinValueValidator(1)])
    CANTIDAD_DISPONIBLE = models.IntegerField(validators=[MinValueValidator(0)])
    # SI CANCELAN LA SALIDARUTA LOS PRODUCTOS SE CANCELAN TAMBIEN. Una devolucion tambien ocasiona que los productos se cancelen
    # CANCELAR UN PRODUCTO ES LO QUE USARE PARA REGRESAR EL PRODUCTO AL STOCK
    STATUS = models.CharField(max_length=100, choices=(("CARGADO", "CARGADO"), ("VENDIDO", "VENDIDO"), ("CANCELADO", "CANCELADO")))
    
    def __str__(self):
        return f"{self.SALIDA_RUTA}, {self.PRODUCTO_RUTA.NOMBRE}"

# Yo diria que esta informacion no guardarla, o al menos eliminarla si se cancela la salidaruta
# Yo digo que esto lo voy a guardar en el localStorage
# Los ire elimenando conforma se cambie su status a visitado
# VOY A TENER DOS ARREGLOS 
# 1 CLEINTES A VISITAR Y CLIENTES DISPONILBLES 
# 2. AL INICIO CLIENTES A VISITAR SE CARGA CON LOS CLIENTES DE LA RUTA 
# 3. CLIENTES DISPONIBLES SON TODOS LOS CLIENTES QUE NO ESTAN EN LA RUTA 
# No tiene el precio, pero accede a ellos mediante su hermano PrecioCliente.
class ClienteSalidaRuta(models.Model):
    # Si la salida ruta se cancela los ClienteSalidaRuta se eliminan
    SALIDA_RUTA = models.ForeignKey(SalidaRuta, on_delete=models.CASCADE, related_name="salida_ruta_clientes")
    # Aqui no uso el objeto cliente porque no ocupo acceder a el para nada. Por ejemplo, no hay que regresar clientes al sotck. Con su nombre me basta (NO ES CORRECTO)
    # LA RAZON POR LA QUE USO EL OBJETO CLIENTE Y NO UN NOMBRE, ES PORQUE EL TENER A FOREIG KEY AL OBJETO CLIENTE ME PERMITE ACCEDER A LOS HERMANOS DE CLIENTESALIDARUTA, ES DECIR, ME PERMITE ACCEDER A LOS PRECIOSCLIENTE
    # LO OTRO QUE QUERÍAS HACER NO FUNCIONARIA SI CAMBIAN EL PRECIO DEL CLIENTE Y LA SALIDARUTA YA SE REGISTRO CON PRECIOS ANTERIORES
    CLIENTE_RUTA = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    STATUS = models.CharField(max_length=100, choices=(("PENDIENTE", "PENDIENTE"), ("VISITADO", "VISITADO"), ("CANCELADO", "CANCELADO")))
    

    def __str__(self):
        return f"{self.SALIDA_RUTA}, {self.CLIENTE_RUTA}"

# NO TE COMPLIQUES LA VIDA. SalidaRuta es igual que Venta. 
# Cuando SalidaRuta no entregue todos sus productos, sera necesario realizar una devolucion
class DevolucionSalidaRuta(models.Model):
    REPARTIDOR = models.CharField(max_length=100, null=True)
    ATIENDE = models.CharField(max_length=100, null=True)
    ADMINISTRADOR = models.CharField(max_length=100, null=True)
    SALIDA_RUTA = models.ForeignKey(SalidaRuta, on_delete=models.CASCADE, related_name="salida_ruta_devoluciones")
    PRODUCTO_DEVOLUCION = models.ForeignKey(Producto, on_delete=models.CASCADE)
    CATIDAD_DEVOLUCION = models.IntegerField(validators=[MinValueValidator(1)])
    # La cajera realiza la devolución, pero mientras el administrador no la autorice, el STATUS permanece como pendiente y la cajera no puede realizar el corte
    STATUS = models.CharField(max_length=100, choices=(("REALIZADO", "REALIZADO"), ("PENDIENTE", "PENDIENTE")))

    def __str__(self):
        return f"{self.SALIDA_RUTA}, {self.CATIDAD_DEVOLUCION}"