from sqlalchemy import Column, Integer, String
from app.extensions import db


class Categoria(db.Model):
    """
    Categorías de productos de la tienda, ej:
    Laptops, Computadoras de Escritorio, Impresoras, Monitores,
    Proyectores, Accesorios, Insumos de Impresión.
    """
    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(255), nullable=True)

    def __repr__(self):
        return self.nombre
