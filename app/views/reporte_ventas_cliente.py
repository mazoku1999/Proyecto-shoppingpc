from app.extensions import db
from flask_appbuilder import BaseView, expose, has_access
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.group import aggregate_sum

from app.models.venta import Venta


class ReporteVentasClienteView(BaseView):
    """
    REPORTE 2 (Integrante 2): Ventas por cliente.
    Consulta: total de ventas (cantidad de órdenes) y monto total
    gastado, agrupado por cliente, ordenado de mayor a menor gasto.
    """

    @expose("/")
    @has_access
    def list(self):
        sql = """
        SELECT
            c.id,
            c.nombre  AS cliente,
            COUNT(v.id)               AS total_ventas,
            COALESCE(SUM(v.total), 0) AS total_gastado
        FROM cliente c
        LEFT JOIN venta v ON v.cliente_id = c.id
        GROUP BY c.id, c.nombre
        ORDER BY total_gastado DESC
        """
        ventas = db.session.execute(db.text(sql)).fetchall()

        return self.render_template(
            "reporte_ventas_cliente.html",
            ventas=ventas,
        )


class VentasPorClienteChartView(GroupByChartView):
    """Gráfica nativa de FAB: total vendido agrupado por cliente."""
    datamodel = SQLAInterface(Venta)
    chart_title = "Total de ventas por cliente"
    label_columns = {"cliente": "Cliente"}
    chart_type = "BarChart"
    definitions = [
        {
            "group": "cliente.nombre",
            "series": [(aggregate_sum, "total")],
        }
    ]
