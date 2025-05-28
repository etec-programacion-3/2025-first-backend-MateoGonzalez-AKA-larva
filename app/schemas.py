from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ----------- USUARIOS -----------

class UsuarioBase(BaseModel):
    nombre: str
    email: str
    rol: Optional[str] = "usuario"

class UsuarioCreate(UsuarioBase): 
    contrasena: str

class UsuarioLogin(BaseModel):
    email: str
    contrasena: str

class UsuarioOut(UsuarioBase):
    id: int
    fecha_registro: datetime

    class Config:
        from_attributes = True

# ----------- LIBROS -----------

class LibroBase(BaseModel):
    titulo: str
    autor: str
    isbn: str
    categoria: str
    estado: str

