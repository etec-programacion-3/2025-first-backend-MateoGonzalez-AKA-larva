from tortoise import fields
from tortoise.models import Model

class Libro(Model):
    id = fields.IntField(pk=True)
    titulo = fields.CharField(max_length=255)
    autor = fields.CharField(max_length=255)
    isbn = fields.CharField(max_length=13, unique=True)
    categoria = fields.CharField(max_length=100)
    estado = fields.CharField(max_length=50)  # Ejemplo: 'disponible', 'prestado'
    fecha_creacion = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} de {self.autor}"

    class Meta:
        table = "libros"  # nombre explícito de la tabla (opcional)

class Usuario(Model):
    id = fields.IntField(pk=True)
    nombre = fields.CharField(max_length=255)
    tipo = fields.CharField(max_length=20)  # estudiante o docente
    email = fields.CharField(max_length=255, unique=True)
    fecha_registro = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Prestamo(Model):
    id = fields.IntField(pk=True)
    usuario = fields.ForeignKeyField("models.Usuario", related_name="prestamos")
    libro = fields.ForeignKeyField("models.Libro", related_name="prestamos")
    fecha_prestamo = fields.DatetimeField(auto_now_add=True)
    fecha_devolucion = fields.DatetimeField(null=True)  # se llena al devolver

    def __str__(self):
        return f"Préstamo de {self.libro.titulo} a {self.usuario.nombre}"

__all__ = ["Libro", "Usuario", "Prestamo"]

# models.py
from tortoise import fields
from tortoise.models import Model

class Usuario(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    fecha_creacion = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"Usuario: {self.email}"
