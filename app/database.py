from tortoise import Tortoise

async def init_db():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["app.models"]},
    )
    print("📚 Base de datos conectada.")
    await Tortoise.generate_schemas()

async def close_db():
    await Tortoise.close_connections()
    print("🔌 Conexión a la base de datos cerrada.")

