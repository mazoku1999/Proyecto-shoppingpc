from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models.proveedor import Proveedor


class ProveedorView(ModelView):
    datamodel = SQLAInterface(Proveedor)
    list_title = "Proveedores"
    add_title = "Nuevo Proveedor"
    edit_title = "Editar Proveedor"
    list_columns = ["nombre", "telefono", "email", "ciudad"]
    add_columns = ["nombre", "telefono", "email", "ciudad"]
    edit_columns = ["nombre", "telefono", "email", "ciudad"]
    show_columns = ["nombre", "telefono", "email", "ciudad"]
    base_permissions = ["can_list", "can_show", "can_add", "can_edit", "can_delete"]
