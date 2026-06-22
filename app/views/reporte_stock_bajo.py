from flask import request
from app.extensions import db
from flask_appbuilder import BaseView, expose, has_access
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.group import aggregate_count

from app.models.producto import Producto


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


class StockPorCategoriaChartView(GroupByChartView):
    """Gráfica nativa de FAB: cantidad de productos por categoría."""
    datamodel = SQLAInterface(Producto)
    chart_title = "Productos por categoría (inventario general)"
    label_columns = {"categoria": "Categoría"}
    chart_type = "ColumnChart"
    definitions = [
        {
            "group": "categoria.nombre",
            "series": [(aggregate_count, "id")],
        }
    ]
