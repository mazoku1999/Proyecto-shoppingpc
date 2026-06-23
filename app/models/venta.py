from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.extensions import db


class Venta(db.Model):
    __tablename__ = "venta"

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    fecha = Column(DateTime, server_default=func.now())
    estado = Column(String(50), nullable=False, default="Pendiente")
    total = Column(Float, nullable=False, default=0)

    cliente = relationship("Cliente", backref="ventas")

    def __repr__(self):
        return f"Venta #{self.id}"
