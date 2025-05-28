from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from app.models import Libro, Usuario
from app.database import init_db, close_db
import bcrypt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas import UsuarioCreate, UsuarioLogin, LibroBase

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()

# -------------------- LIBROS --------------------

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

# -------------------- USUARIOS --------------------

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

# -------------------- REGISTRO --------------------

@app.post("/registro")
async def registro(usuario: UsuarioCreate):
    if await Usuario.filter(email=usuario.email).exists():
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    nuevo_usuario = Usuario()
    hashed_password = nuevo_usuario.hash_contrasena(usuario.contrasena)

    nuevo_usuario = await Usuario.create(
        nombre=usuario.nombre,
        email=usuario.email,
        contrasena=hashed_password,
        rol=usuario.rol or "usuario"
    )

    return {"mensaje": "Usuario creado con éxito", "usuario": nuevo_usuario.email}

# -------------------- LOGIN --------------------

@app.post("/login")
async def login(usuario: UsuarioLogin):
    user = await Usuario.get_or_none(email=usuario.email)
    if not user or not user.verificar_contrasena(usuario.contrasena):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"mensaje": "Inicio de sesión exitoso", "rol": user.rol}

# -------------------- DB CONFIG --------------------

register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['app.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)
from fastapi import Depends, Header
from typing import Optional

async def get_current_user(x_email: Optional[str] = Header(None)):
    if not x_email:
        raise HTTPException(status_code=401, detail="No se proporcionó el email")

    user = await Usuario.get_or_none(email=x_email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user

async def admin_required(user: Usuario = Depends(get_current_user)):
    if user.rol != "admin":
        raise HTTPException(status_code=403, detail="Permisos insuficientes")
    return user

