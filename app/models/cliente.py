from sqlalchemy import Column, Integer, String
from app.extensions import db


class Cliente(db.Model):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(150), nullable=False)
    email = Column(String(120), nullable=True)
    telefono = Column(String(20), nullable=True)
    direccion = Column(String(255), nullable=True)
    nit_ci = Column(String(30), nullable=True)

    def __repr__(self):
        return self.nombre
