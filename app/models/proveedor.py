from sqlalchemy import Column, Integer, String
from app.extensions import db


class Proveedor(db.Model):
    __tablename__ = "proveedor"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(150), nullable=False)
    telefono = Column(String(20), nullable=True)
    email = Column(String(120), nullable=True)
    ciudad = Column(String(80), nullable=True)

    def __repr__(self):
        return self.nombre
