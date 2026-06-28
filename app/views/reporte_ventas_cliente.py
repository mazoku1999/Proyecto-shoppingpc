from app.extensions import db
from flask_appbuilder import BaseView, expose, has_access
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.group import aggregate_sum

from app.models.venta import Venta
from app.services.gemini_service import generate_forecasts



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


class VentasPorClienteChartView(BaseView):
    """Gráfica personalizada con Chart.js: total vendido agrupado por cliente."""
    
    @expose("/")
    @has_access
    def list(self):
        sql = """
        SELECT c.nombre AS cliente, COALESCE(SUM(v.total), 0) AS total_ventas
        FROM cliente c
        INNER JOIN venta v ON v.cliente_id = c.id
        GROUP BY c.id, c.nombre
        ORDER BY total_ventas DESC
        """
        data = db.session.execute(db.text(sql)).fetchall()
        
        total_recaudado = sum(item[1] for item in data)
        max_item = max(data, key=lambda x: x[1]) if data else (None, 0)
        min_item = min(data, key=lambda x: x[1]) if data else (None, 0)
        promedio_cliente = total_recaudado / len(data) if data else 0
        
        stats = {
            "total_recaudado": float(total_recaudado),
            "max_nombre": max_item[0],
            "max_monto": float(max_item[1]),
            "max_pct": round((max_item[1] / total_recaudado * 100), 1) if total_recaudado > 0 else 0,
            "min_nombre": min_item[0],
            "min_monto": float(min_item[1]),
            "min_pct": round((min_item[1] / total_recaudado * 100), 1) if total_recaudado > 0 else 0,
            "promedio": round(promedio_cliente, 2),
            "cantidad_clientes": len(data),
        }
        
        labels = [item[0] for item in data]
        values = [float(item[1]) for item in data]
        
        # Generar resumen de datos para la IA
        summary_parts = []
        for item in data:
            pct = round((float(item[1]) / float(total_recaudado) * 100), 1) if total_recaudado > 0 else 0
            summary_parts.append(f"{item[0]}: {float(item[1]):.2f} Bs ({pct}%)")
        data_summary = f"Total facturado: {float(total_recaudado):.2f} Bs. Ventas por cliente: {', '.join(summary_parts)}."
        
        forecasts = generate_forecasts("Ventas por Cliente", data_summary)
        
        return self.render_template(
            "chart_ventas_cliente.html",
            labels=labels,
            values=values,
            stats=stats,
            forecasts=forecasts
        )

