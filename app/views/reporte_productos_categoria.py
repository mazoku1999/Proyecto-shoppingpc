from flask import request
from app.extensions import db, appbuilder
from flask_appbuilder import BaseView, expose, has_access
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.group import aggregate_count

from app.models.categoria import Categoria
from app.models.producto import Producto


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


class ProductosPorCategoriaChartView(GroupByChartView):
    """Gráfica nativa de FAB: productos agrupados por categoría."""
    datamodel = SQLAInterface(Producto)
    chart_title = "Cantidad de productos por categoría"
    label_columns = {"categoria": "Categoría"}
    chart_type = "PieChart"
    definitions = [
        {
            "group": "categoria.nombre",
            "series": [(aggregate_count, "id")],
        }
    ]
