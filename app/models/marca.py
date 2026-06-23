from sqlalchemy import Column, Integer, String
from app.extensions import db


class Marca(db.Model):
    """
    Marcas tecnológicas que vende la tienda, ej:
    HP, EPSON, ASUS, Samsung, Logitech, Dell, Lenovo.
    """
    __tablename__ = "marca"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False, unique=True)
    pais_origen = Column(String(80), nullable=True)

    def __repr__(self):
        return self.nombre
