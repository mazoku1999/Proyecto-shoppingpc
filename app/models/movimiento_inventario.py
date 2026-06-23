from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.extensions import db


class MovimientoInventario(db.Model):
    __tablename__ = "movimiento_inventario"

    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey("producto.id"), nullable=False)
    tipo = Column(String(20), nullable=False)  # "Entrada" o "Salida"
    cantidad = Column(Integer, nullable=False)
    fecha = Column(DateTime, server_default=func.now())
    motivo = Column(String(255), nullable=True)

    producto = relationship("Producto", backref="movimientos")

    def __repr__(self):
        return f"Movimiento #{self.id}"
