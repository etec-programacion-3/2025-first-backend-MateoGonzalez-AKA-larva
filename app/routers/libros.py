from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database
from typing import List, Optional

router = APIRouter(
    prefix="/libros",
    tags=["Libros"]
)

# Obtener la base de datos
get_db = database.get_db

# Crear un libro
@router.post("/", response_model=schemas.LibroResponse)
def crear_libro(libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    nuevo_libro = models.Libro(**libro.dict())
    db.add(nuevo_libro)
    db.commit()
    db.refresh(nuevo_libro)
    return nuevo_libro

# Obtener todos los libros con búsqueda y filtrado
@router.get("/", response_model=List[schemas.LibroResponse])
def obtener_libros(
    autor: Optional[str] = None,
    anio: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Libro)
    if autor:
        query = query.filter(models.Libro.autor.ilike(f"%{autor}%"))
    if anio:
        query = query.filter(models.Libro.anio == anio)
    return query.all()

# Obtener un solo libro por ID
@router.get("/{libro_id}", response_model=schemas.LibroResponse)
def obtener_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

# Actualizar un libro por ID
@router.put("/{libro_id}", response_model=schemas.LibroResponse)
def actualizar_libro(libro_id: int, datos: schemas.LibroCreate, db: Session = Depends(get_db)):
    libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    for key, value in datos.dict().items():
        setattr(libro, key, value)
    db.commit()
    db.refresh(libro)
    return libro

# Eliminar un libro por ID
@router.delete("/{libro_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    db.delete(libro)
    db.commit()
