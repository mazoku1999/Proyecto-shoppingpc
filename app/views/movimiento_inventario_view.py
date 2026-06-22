from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models.movimiento_inventario import MovimientoInventario


class MovimientoInventarioView(ModelView):
    datamodel = SQLAInterface(MovimientoInventario)
    list_title = "Movimientos de Inventario"
    add_title = "Nuevo Movimiento"
    edit_title = "Editar Movimiento"
    list_columns = ["producto", "tipo", "cantidad", "fecha", "motivo"]
    add_columns = ["producto", "tipo", "cantidad", "motivo"]
    edit_columns = ["producto", "tipo", "cantidad", "motivo"]
    show_columns = ["producto", "tipo", "cantidad", "fecha", "motivo"]
    base_permissions = ["can_list", "can_show", "can_add", "can_edit", "can_delete"]
