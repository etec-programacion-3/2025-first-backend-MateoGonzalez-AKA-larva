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
