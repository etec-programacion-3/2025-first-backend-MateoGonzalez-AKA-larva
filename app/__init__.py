# app/__init__.py

# Puedes importar módulos aquí si los necesitas globalmente, por ejemplo:
from .models import Libro, Usuario
from .database import init_db, close_db
from .schemas import UsuarioCreate, UsuarioLogin, UsuarioOut, LibroBase
