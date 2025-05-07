from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from app.models import Libro
from app.database import init_db, close_db
from app.models import Usuario


app = FastAPI()

# Configurar la base de datos
@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()

# Endpoints de CRUD
@app.get("/libros")
async def get_libros():
    libros = await Libro.all()
    return libros

@app.get("/libros/{id}")
async def get_libro(id: int):
    libro = await Libro.get_or_none(id=id)
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@app.post("/libros")
async def create_libro(titulo: str, autor: str, isbn: str, categoria: str, estado: str):
    libro = await Libro.create(
        titulo=titulo,
        autor=autor,
        isbn=isbn,
        categoria=categoria,
        estado=estado
    )
    return libro

@app.put("/libros/{id}")
async def update_libro(id: int, titulo: str, autor: str, isbn: str, categoria: str, estado: str):
    libro = await Libro.get_or_none(id=id)
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    libro.titulo = titulo
    libro.autor = autor
    libro.isbn = isbn
    libro.categoria = categoria
    libro.estado = estado
    await libro.save()
    return libro

@app.delete("/libros/{id}")
async def delete_libro(id: int):
    libro = await Libro.get_or_none(id=id)
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    await libro.delete()
    return {"message": "Libro eliminado"}

# Configuración para la base de datos
register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['app.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.get("/usuarios")
async def get_usuarios():
    return await Usuario.all()

@app.get("/usuarios/{id}")
async def get_usuario(id: int):
    return await Usuario.get(id=id)

@app.post("/usuarios")
async def create_usuario(nombre: str, tipo: str, email: str):
    return await Usuario.create(nombre=nombre, tipo=tipo, email=email)

@app.put("/usuarios/{id}")
async def update_usuario(id: int, nombre: str, tipo: str, email: str):
    usuario = await Usuario.get(id=id)
    usuario.nombre = nombre
    usuario.tipo = tipo
    usuario.email = email
    await usuario.save()
    return usuario

@app.delete("/usuarios/{id}")
async def delete_usuario(id: int):
    usuario = await Usuario.get(id=id)
    await usuario.delete()
    return {"message": "Usuario eliminado"}

# main.py
import bcrypt
from fastapi import HTTPException, status
from app.models import Usuario
from app.schemas import UsuarioCrear, UsuarioLogin
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Crear un nuevo usuario
@app.post("/registro")
async def registro(usuario: UsuarioCrear):
    # Verificar si ya existe un usuario con el mismo email
    if await Usuario.filter(email=usuario.email).exists():
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    # Hashear la contraseña
    hashed_password = bcrypt.hashpw(usuario.password.encode('utf-8'), bcrypt.gensalt())
    
    # Crear el usuario
    nuevo_usuario = await Usuario.create(email=usuario.email, password=hashed_password)
    
    return {"mensaje": "Usuario creado con éxito", "usuario": nuevo_usuario.email}

# Iniciar sesión
@app.post("/login")
async def login(usuario: UsuarioLogin):
    # Verificar si el usuario existe
    user = await Usuario.get_or_none(email=usuario.email)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    # Verificar la contraseña
    if not bcrypt.checkpw(usuario.password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    return {"mensaje": "Inicio de sesión exitoso"}
