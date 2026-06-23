from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db


class DetalleVenta(db.Model):
    __tablename__ = "detalle_venta"

    id = Column(Integer, primary_key=True)
    venta_id = Column(Integer, ForeignKey("venta.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("producto.id"), nullable=False)
    cantidad = Column(Integer, nullable=False, default=1)
    precio_unitario = Column(Float, nullable=False, default=0)

    venta = relationship("Venta", backref="detalles")
    producto = relationship("Producto", backref="detalles_venta")

    def __repr__(self):
        return f"Detalle #{self.id}"
