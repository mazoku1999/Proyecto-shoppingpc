from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models.venta import Venta
from app.models.detalle_venta import DetalleVenta


class DetalleVentaView(ModelView):
    datamodel = SQLAInterface(DetalleVenta)
    list_title = "Detalle de Ventas"
    list_columns = ["venta", "producto", "cantidad", "precio_unitario"]
    add_columns = ["venta", "producto", "cantidad", "precio_unitario"]
    edit_columns = ["venta", "producto", "cantidad", "precio_unitario"]
    show_columns = ["venta", "producto", "cantidad", "precio_unitario"]
    base_permissions = ["can_list", "can_show", "can_add", "can_edit", "can_delete"]


class VentaView(ModelView):
    datamodel = SQLAInterface(Venta)
    list_title = "Ventas Realizadas"
    add_title = "Nueva Venta"
    edit_title = "Editar Venta"
    list_columns = ["id", "cliente", "fecha", "estado", "total"]
    add_columns = ["cliente", "estado", "total"]
    edit_columns = ["cliente", "estado", "total"]
    show_columns = ["id", "cliente", "fecha", "estado", "total"]
    related_views = [DetalleVentaView]
    base_permissions = ["can_list", "can_show", "can_add", "can_edit", "can_delete"]
