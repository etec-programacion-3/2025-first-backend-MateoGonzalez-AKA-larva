from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from app.models import Libro, Usuario
from app.database import init_db, close_db
import bcrypt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas import UsuarioCreate, UsuarioLogin, LibroBase
from typing import Optional

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O podés poner "http://localhost:5500" si usás Live Server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Configuración CORS para permitir requests desde frontend
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:8000",  # agregá el puerto del backend por las dudas
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # o ["*"] para todos los orígenes (solo pruebas)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()

# (Acá va el resto de tus rutas...)

register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['app.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)

# (Dependencias, endpoints, etc.)
