# app/db.py
from tortoise import Tortoise

async def init():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',  # Ruta de la base de datos SQLite
        modules={'models': ['app.models']}  # Ruta del modelo
    )
    await Tortoise.generate_schemas()

async def close():
    await Tortoise.close_connections()
