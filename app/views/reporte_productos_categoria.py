from flask import request
from app.extensions import db, appbuilder
from flask_appbuilder import BaseView, expose, has_access
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.group import aggregate_count

from app.models.categoria import Categoria
from app.models.producto import Producto
from app.services.gemini_service import generate_forecasts



class ReporteProductosCategoriaView(BaseView):
    """
    REPORTE 1 (Integrante 1): Productos por categoría.
    Consulta: si el usuario seleccionó una categoría (Laptops,
    Impresoras, Monitores, etc.), filtramos por esa categoría;
    si no, traemos todos los productos del catálogo.
    """

    @expose("/", methods=["GET", "POST"])
    @has_access
    def list(self):
        # 1. Traer todas las categorías para el select
        categorias = db.session.query(Categoria).all()

        # 2. Capturar la categoría seleccionada
        seleccionado = request.form.get("cat_id")

        # 3. Lógica: Si seleccionó categoría filtra; si no, trae todos.
        if seleccionado and seleccionado != "" and seleccionado != "None":
            sql = """
            SELECT p.id, p.nombre, p.modelo, p.precio, p.stock,
                   c.nombre AS categoria, m.nombre AS marca
            FROM producto p
            INNER JOIN categoria c ON p.categoria_id = c.id
            LEFT  JOIN marca m     ON p.marca_id = m.id
            WHERE p.categoria_id = :id
            ORDER BY p.nombre
            """
            productos = db.session.execute(db.text(sql), {"id": seleccionado}).fetchall()
        else:
            sql = """
            SELECT p.id, p.nombre, p.modelo, p.precio, p.stock,
                   c.nombre AS categoria, m.nombre AS marca
            FROM producto p
            INNER JOIN categoria c ON p.categoria_id = c.id
            LEFT  JOIN marca m     ON p.marca_id = m.id
            ORDER BY p.nombre
            """
            productos = db.session.execute(db.text(sql)).fetchall()
            seleccionado = ""  # Normalizamos a vacío para el template

        # 4. Enviar datos al template
        return self.render_template(
            "reporte_productos_categoria.html",
            categorias=categorias,
            productos=productos,
            seleccionado=seleccionado,
        )


class ProductosPorCategoriaChartView(BaseView):
    """Gráfica personalizada con Chart.js: productos agrupados por categoría."""
    
    @expose("/")
    @has_access
    def list(self):
        sql = """
        SELECT c.nombre AS categoria, COUNT(p.id) AS cantidad
        FROM producto p
        INNER JOIN categoria c ON p.categoria_id = c.id
        GROUP BY c.id, c.nombre
        """
        data = db.session.execute(db.text(sql)).fetchall()
        
        total_productos = sum(item[1] for item in data)
        max_item = max(data, key=lambda x: x[1]) if data else (None, 0)
        min_item = min(data, key=lambda x: x[1]) if data else (None, 0)
        
        stats = {
            "total": total_productos,
            "max_nombre": max_item[0],
            "max_cantidad": max_item[1],
            "max_pct": round((max_item[1] / total_productos * 100), 1) if total_productos > 0 else 0,
            "min_nombre": min_item[0],
            "min_cantidad": min_item[1],
            "min_pct": round((min_item[1] / total_productos * 100), 1) if total_productos > 0 else 0,
        }
        
        labels = [item[0] for item in data]
        values = [item[1] for item in data]
        
        # Generar resumen de datos para la IA
        summary_parts = []
        for item in data:
            pct = round((item[1] / total_productos * 100), 1) if total_productos > 0 else 0
            summary_parts.append(f"{item[0]}: {item[1]} unidades ({pct}%)")
        data_summary = f"Total de productos en catálogo: {total_productos}. Distribución por categorías: {', '.join(summary_parts)}."
        
        forecasts = generate_forecasts("Distribución de Productos por Categoría", data_summary)
        
        return self.render_template(
            "chart_productos_categoria.html",
            labels=labels,
            values=values,
            stats=stats,
            forecasts=forecasts
        )

