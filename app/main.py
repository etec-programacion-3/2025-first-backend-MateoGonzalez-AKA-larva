from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.contrib.fastapi import register_tortoise
from app.models import Libro, Usuario
from app.schemas import UsuarioCrear, UsuarioLogin
from app.database import init_db, close_db
import bcrypt

app = FastAPI()

# Eventos de inicio y cierre
@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()

# ----------- LIBROS -----------

@app.get("/libros")
async def get_libros():
    return await Libro.all()

@app.get("/libros/{id}")
async def get_libro(id: int):
    libro = await Libro.get_or_none(id=id)
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@app.post("/libros")
async def create_libro(titulo: str, autor: str, isbn: str, categoria: str, estado: str):
    return await Libro.create(
        titulo=titulo,
        autor=autor,
        isbn=isbn,
        categoria=categoria,
        estado=estado
    )

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
    return {"mensaje": "Libro eliminado"}

# ----------- USUARIOS -----------

@app.get("/usuarios")
async def get_usuarios():
    return await Usuario.all()

@app.get("/usuarios/{id}")
async def get_usuario(id: int):
    usuario = await Usuario.get_or_none(id=id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.post("/usuarios")
async def create_usuario(nombre: str, tipo: str, email: str, password: str):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return await Usuario.create(nombre=nombre, tipo=tipo, email=email, password=hashed_password.decode("utf-8"))


@app.put("/usuarios/{id}")
async def update_usuario(id: int, nombre: str, tipo: str, email: str):
    usuario = await Usuario.get_or_none(id=id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.nombre = nombre
    usuario.tipo = tipo
    usuario.email = email
    await usuario.save()
    return usuario

@app.delete("/usuarios/{id}")
async def delete_usuario(id: int):
    usuario = await Usuario.get_or_none(id=id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    await usuario.delete()
    return {"mensaje": "Usuario eliminado"}

# ----------- AUTENTICACIÓN -----------

@app.post("/registro")
async def registro(usuario: UsuarioCrear):
    if await Usuario.filter(email=usuario.email).exists():
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    hashed_password = bcrypt.hashpw(usuario.password.encode('utf-8'), bcrypt.gensalt())
    nuevo_usuario = await Usuario.create(
        email=usuario.email,
        nombre=usuario.nombre,
        tipo=usuario.tipo,
        password=hashed_password.decode('utf-8')
    )
    return {"mensaje": "Usuario registrado", "usuario": nuevo_usuario.email}

@app.post("/login")
async def login(usuario: UsuarioLogin):
    user = await Usuario.get_or_none(email=usuario.email)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    if not bcrypt.checkpw(usuario.password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    return {"mensaje": "Inicio de sesión exitoso"}

# ----------- CONFIGURACIÓN TORTOISE -----------

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
