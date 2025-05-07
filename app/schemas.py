from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ----------- USUARIOS -----------

class UsuarioBase(BaseModel):
    nombre: str
    email: str

class UsuarioCreate(UsuarioBase):
    contrasena: str

class UsuarioLogin(BaseModel):
    email: str
    contrasena: str

class UsuarioOut(UsuarioBase):
    id: int
    fecha_registro: datetime

    class Config:
        orm_mode = True

# ----------- LIBROS -----------

class LibroBase(BaseModel):
    titulo: str
    autor: str
    isbn: str
    categoria: str
    estado: str

class LibroCreate(LibroBase):
    pass

class LibroOut(LibroBase):
    id: int
    fecha_creacion: datetime

    class Config:
        orm_mode = True

# ----------- PRÉSTAMOS -----------

class PrestamoCreate(BaseModel):
    usuario_id: int
    libro_id: int

class PrestamoOut(BaseModel):
    id: int
    fecha_prestamo: datetime
    fecha_devolucion: Optional[datetime]
    usuario: UsuarioOut
    libro: LibroOut

    class Config:
        orm_mode = True
from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    contrasena: str

class UsuarioLogin(BaseModel):
    email: str
    contrasena: str

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str

