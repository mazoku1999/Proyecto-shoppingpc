from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db


class Producto(db.Model):
    __tablename__ = "producto"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(180), nullable=False)
    modelo = Column(String(100), nullable=True)
    precio = Column(Float, nullable=False, default=0)
    stock = Column(Integer, nullable=False, default=0)

    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)
    marca_id = Column(Integer, ForeignKey("marca.id"), nullable=True)
    proveedor_id = Column(Integer, ForeignKey("proveedor.id"), nullable=True)

    categoria = relationship("Categoria", backref="productos")
    marca = relationship("Marca", backref="productos")
    proveedor = relationship("Proveedor", backref="productos")

    def __repr__(self):
        return self.nombre
