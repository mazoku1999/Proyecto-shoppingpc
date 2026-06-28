from flask import request
from app.extensions import db
from flask_appbuilder import BaseView, expose, has_access
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.group import aggregate_count

from app.models.producto import Producto
from app.services.gemini_service import generate_forecasts



class ReporteStockBajoView(BaseView):
    """
    REPORTE 3 (Integrante 3): Productos con stock bajo.
    Consulta: laptops, impresoras, monitores, etc. cuyo stock
    está por debajo de un mínimo configurable (parámetro "minimo",
    por defecto 5 unidades, típico en equipos de cómputo).
    """

    @expose("/", methods=["GET", "POST"])
    @has_access
    def list(self):
        # Capturar el umbral mínimo (editable en el formulario)
        minimo = request.values.get("minimo")

        if minimo and minimo.isdigit():
            minimo = int(minimo)
        else:
            minimo = 5  # valor por defecto para equipos de cómputo

        sql = """
        SELECT p.id, p.nombre, p.modelo, p.stock,
               c.nombre AS categoria,
               m.nombre AS marca
        FROM producto p
        INNER JOIN categoria c ON p.categoria_id = c.id
        LEFT  JOIN marca m     ON p.marca_id = m.id
        WHERE p.stock < :minimo
        ORDER BY p.stock ASC
        """
        productos = db.session.execute(db.text(sql), {"minimo": minimo}).fetchall()

        return self.render_template(
            "reporte_stock_bajo.html",
            productos=productos,
            minimo=minimo,
        )


class StockPorCategoriaChartView(BaseView):
    """Gráfica personalizada con Chart.js: cantidad de stock de productos por categoría."""
    
    @expose("/")
    @has_access
    def list(self):
        sql = """
        SELECT c.nombre AS categoria, COALESCE(SUM(p.stock), 0) AS total_stock
        FROM producto p
        INNER JOIN categoria c ON p.categoria_id = c.id
        GROUP BY c.id, c.nombre
        """
        data = db.session.execute(db.text(sql)).fetchall()
        
        total_stock = sum(item[1] for item in data)
        max_item = max(data, key=lambda x: x[1]) if data else (None, 0)
        min_item = min(data, key=lambda x: x[1]) if data else (None, 0)
        
        stats = {
            "total": int(total_stock),
            "max_nombre": max_item[0],
            "max_cantidad": int(max_item[1]),
            "max_pct": round((max_item[1] / total_stock * 100), 1) if total_stock > 0 else 0,
            "min_nombre": min_item[0],
            "min_cantidad": int(min_item[1]),
            "min_pct": round((min_item[1] / total_stock * 100), 1) if total_stock > 0 else 0,
        }
        
        labels = [item[0] for item in data]
        values = [int(item[1]) for item in data]
        
        # Generar resumen de datos para la IA
        summary_parts = []
        for item in data:
            pct = round((int(item[1]) / int(total_stock) * 100), 1) if total_stock > 0 else 0
            summary_parts.append(f"{item[0]}: {int(item[1])} unidades ({pct}%)")
        data_summary = f"Total en stock: {int(total_stock)} unidades. Stock por categorías: {', '.join(summary_parts)}."
        
        forecasts = generate_forecasts("Stock de Inventario por Categoría", data_summary)
        
        return self.render_template(
            "chart_stock_categoria.html",
            labels=labels,
            values=values,
            stats=stats,
            forecasts=forecasts
        )

