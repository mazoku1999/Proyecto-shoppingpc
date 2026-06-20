from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models.categoria import Categoria


class CategoriaView(ModelView):
    datamodel = SQLAInterface(Categoria)
    list_title = "Categorías de Productos"
    add_title = "Nueva Categoría"
    edit_title = "Editar Categoría"
    list_columns = ["nombre", "descripcion"]
    add_columns = ["nombre", "descripcion"]
    edit_columns = ["nombre", "descripcion"]
    show_columns = ["nombre", "descripcion"]
    base_permissions = ["can_list", "can_show", "can_add", "can_edit", "can_delete"]
