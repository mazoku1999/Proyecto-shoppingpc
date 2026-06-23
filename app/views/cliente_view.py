from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models.cliente import Cliente


class ClienteView(ModelView):
    datamodel = SQLAInterface(Cliente)
    list_title = "Clientes"
    add_title = "Nuevo Cliente"
    edit_title = "Editar Cliente"
    list_columns = ["nombre", "email", "telefono", "nit_ci"]
    add_columns = ["nombre", "email", "telefono", "direccion", "nit_ci"]
    edit_columns = ["nombre", "email", "telefono", "direccion", "nit_ci"]
    show_columns = ["nombre", "email", "telefono", "direccion", "nit_ci"]
    base_permissions = ["can_list", "can_show", "can_add", "can_edit", "can_delete"]
