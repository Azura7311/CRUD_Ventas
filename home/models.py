from django.db import models

class Producto(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    inventario = models.IntegerField()

    def __str__(self):
        return f"{self.id} - {self.nombre} - {str(self.precio)} - {str(self.inventario)}"

class Compra(models.Model):
    recibo = models.IntegerField()
    producto_id = models.CharField(max_length=5)
    cantidad = models.IntegerField()
    total = models.IntegerField()

class Recibo(models.Model):
    cliente = models.CharField(max_length=100)
    id_cliente = models.IntegerField()
    email = models.CharField(max_length=100)
    metodo_pago = models.CharField(max_length=100)
    num_productos = models.IntegerField()
    monto = models.IntegerField()
    fecha = models.DateTimeField(auto_now=True)
    total = models.IntegerField()

    def __str__(self):
        return f"{self.cliente} - {self.total}"