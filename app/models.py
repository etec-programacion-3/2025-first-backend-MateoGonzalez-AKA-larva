from tortoise import fields
from tortoise.models import Model
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Usuario(Model):
    id = fields.IntField(pk=True)
    nombre = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    contrasena = fields.CharField(max_length=255)
    rol = fields.CharField(max_length=50, default="usuario")
    fecha_registro = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    def hash_contrasena(self, contrasena: str):
        return pwd_context.hash(contrasena)

    def verificar_contrasena(self, contrasena: str):
        return pwd_context.verify(contrasena, self.contrasena)

class Libro(Model):
    id = fields.IntField(pk=True)
    titulo = fields.CharField(max_length=255)
    autor = fields.CharField(max_length=255)
    isbn = fields.CharField(max_length=13, unique=True)
    categoria = fields.CharField(max_length=100)
    estado = fields.CharField(max_length=50)
    fecha_creacion = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} de {self.autor}"

    class Meta:
        table = "libros"

class Prestamo(Model):
    id = fields.IntField(pk=True)
    usuario = fields.ForeignKeyField("models.Usuario", related_name="prestamos")
    libro = fields.ForeignKeyField("models.Libro", related_name="prestamos")
    fecha_prestamo = fields.DatetimeField(auto_now_add=True)
    fecha_devolucion = fields.DatetimeField(null=True)

    def __str__(self):
        return f"Préstamo de {self.libro.titulo} a {self.usuario.nombre}"

__all__ = ["Libro", "Usuario", "Prestamo"]

