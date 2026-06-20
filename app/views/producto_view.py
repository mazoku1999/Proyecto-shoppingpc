from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models.producto import Producto

class ProductoView(ModelView):
    datamodel = SQLAInterface(Producto)

    list_title = "Catálogo de Productos"
    add_title = "Nuevo Producto"
    edit_title = "Editar Producto"

    # 🔥 SOLO CAMPOS SIMPLES EN LISTADO
    list_columns = [
        "nombre",
        "modelo",
        "marca",
        "categoria.nombre",
        "precio",
        "stock"
    ]

    # 🔥 EN FORMULARIOS SE USA EL ID (RELACIÓN)
    add_columns = [
        "nombre",
        "modelo",
        "categoria",
        "marca",
        "proveedor",
        "precio",
        "stock"
    ]

    edit_columns = [
        "nombre",
        "modelo",
        "categoria",
        "marca",
        "proveedor",
        "precio",
        "stock"
    ]

    # 🔥 EN DETALLE TAMBIÉN SE USA NOMBRE LEGIBLE
    show_columns = [
        "nombre",
        "modelo",
        "categoria.nombre",
        "marca",
        "proveedor",
        "precio",
        "stock"
    ]

    search_columns = ["nombre", "modelo"]

    base_permissions = [
        "can_list",
        "can_show",
        "can_add",
        "can_edit",
        "can_delete"
    ]











# class ProductoView(ModelView):
#     datamodel = SQLAInterface(Producto)
#     list_title = "Catálogo de Productos"
#     add_title = "Nuevo Producto"
#     edit_title = "Editar Producto"
#     list_columns = ["nombre", "modelo", "marca", "categoria", "precio", "stock"]
#     add_columns = ["nombre", "modelo", "categoria", "marca", "proveedor", "precio", "stock"]
#     edit_columns = ["nombre", "modelo", "categoria", "marca", "proveedor", "precio", "stock"]
#     show_columns = ["nombre", "modelo", "categoria", "marca", "proveedor", "precio", "stock"]
#     search_columns = ["nombre", "modelo"]
#     base_permissions = ["can_list", "can_show", "can_add", "can_edit", "can_delete"]
