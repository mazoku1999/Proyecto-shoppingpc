from flask import Flask
from .extensions import appbuilder, db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config")
    db.init_app(app)

    with app.app_context():
        appbuilder.init_app(app, db.session)

        # ------------------------------------------------------------
        # Importar modelos (necesario para que SQLAlchemy los registre
        # antes de db.create_all())
        # ------------------------------------------------------------
        from app.models.categoria import Categoria
        from app.models.marca import Marca
        from app.models.proveedor import Proveedor
        from app.models.producto import Producto
        from app.models.cliente import Cliente
        from app.models.venta import Venta
        from app.models.detalle_venta import DetalleVenta
        from app.models.movimiento_inventario import MovimientoInventario

        db.create_all()

        # ------------------------------------------------------------
        # Importar vistas
        # ------------------------------------------------------------
        from app.views import (
            CategoriaView,
            MarcaView,
            ProveedorView,
            ProductoView,
            ClienteView,
            VentaView,
            DetalleVentaView,
            MovimientoInventarioView,
        )
        from app.views.reporte_productos_categoria import (
            ReporteProductosCategoriaView,
            ProductosPorCategoriaChartView,
        )
        from app.views.reporte_ventas_cliente import (
            ReporteVentasClienteView,
            VentasPorClienteChartView,
        )
        from app.views.reporte_stock_bajo import (
            ReporteStockBajoView,
            StockPorCategoriaChartView,
        )

        # ------------------------------------------------------------
        # Registro de vistas — Catálogo
        # ------------------------------------------------------------
        appbuilder.add_view(
            CategoriaView,
            "Categorías",
            icon="fa-tags",
            category="Catálogo",
        )
        appbuilder.add_view(
            MarcaView,
            "Marcas",
            icon="fa-trademark",
            category="Catálogo",
        )
        appbuilder.add_view(
            ProveedorView,
            "Proveedores",
            icon="fa-truck",
            category="Catálogo",
        )
        appbuilder.add_view(
            ProductoView,
            "Productos",
            icon="fa-desktop",
            category="Catálogo",
        )

        # ------------------------------------------------------------
        # Registro de vistas — Ventas
        # ------------------------------------------------------------
        appbuilder.add_view(
            ClienteView,
            "Clientes",
            icon="fa-user",
            category="Ventas",
        )
        appbuilder.add_view(
            VentaView,
            "Ventas",
            icon="fa-shopping-cart",
            category="Ventas",
        )
        appbuilder.add_view_no_menu(DetalleVentaView)

        # ------------------------------------------------------------
        # Registro de vistas — Inventario
        # ------------------------------------------------------------
        appbuilder.add_view(
            MovimientoInventarioView,
            "Movimientos de Inventario",
            icon="fa-exchange",
            category="Inventario",
        )

        # ------------------------------------------------------------
        # Registro de reportes (uno por integrante)
        # ------------------------------------------------------------
        appbuilder.add_view(
            ReporteProductosCategoriaView,
            "Productos por Categoría",
            icon="fa-list-alt",
            category="Reportes",
        )
        appbuilder.add_view(
            ProductosPorCategoriaChartView,
            "Gráfica: Productos por Categoría",
            icon="fa-pie-chart",
            category="Reportes",
        )
        appbuilder.add_view(
            ReporteVentasClienteView,
            "Ventas por Cliente",
            icon="fa-money",
            category="Reportes",
        )
        appbuilder.add_view(
            VentasPorClienteChartView,
            "Gráfica: Ventas por Cliente",
            icon="fa-bar-chart",
            category="Reportes",
        )
        appbuilder.add_view(
            ReporteStockBajoView,
            "Stock Bajo",
            icon="fa-warning",
            category="Reportes",
        )
        appbuilder.add_view(
            StockPorCategoriaChartView,
            "Gráfica: Stock por Categoría",
            icon="fa-bar-chart",
            category="Reportes",
        )

        # ------------------------------------------------------------
        # Crear roles Supervisor y Usuario si no existen
        # (Admin ya existe por defecto en Flask-AppBuilder)
        # ------------------------------------------------------------
        configurar_roles()

    return app


def configurar_roles():
    """
    Crea los roles Supervisor y Usuario y les asigna permisos
    diferenciados sobre las vistas del sistema.

    Admin   → acceso total (rol de fábrica de Flask-AppBuilder).
    Supervisor → catálogo, ventas, inventario y reportes;
                 puede crear y editar pero NO eliminar.
    Usuario    → solo catálogo (consulta) y ventas (crear);
                 no ve inventario, proveedores ni reportes.
    """
    sm = appbuilder.sm

    # --- Supervisor -------------------------------------------------
    rol_supervisor = sm.find_role("Supervisor") or sm.add_role("Supervisor")

    vistas_supervisor = [
        "CategoriaView", "MarcaView", "ProveedorView", "ProductoView",
        "ClienteView", "VentaView", "DetalleVentaView",
        "MovimientoInventarioView",
        "ReporteProductosCategoriaView", "ProductosPorCategoriaChartView",
        "ReporteVentasClienteView", "VentasPorClienteChartView",
        "ReporteStockBajoView", "StockPorCategoriaChartView",
    ]
    for vista in vistas_supervisor:
        for permiso in ["can_list", "can_show", "can_add", "can_edit", "can_chart"]:
            pvm = sm.find_permission_view_menu(permiso, vista)
            if pvm:
                sm.add_permission_role(rol_supervisor, pvm)

    # Menús autorizados para Supervisor (excluye Seguridad/Security)
    menus_supervisor = [
        "Catálogo", "Categorías", "Marcas", "Proveedores", "Productos",
        "Ventas", "Clientes",
        "Inventario", "Movimientos de Inventario",
        "Reportes", "Productos por Categoría", "Gráfica: Productos por Categoría",
        "Ventas por Cliente", "Gráfica: Ventas por Cliente", "Stock Bajo", "Gráfica: Stock por Categoría"
    ]
    for menu_name in menus_supervisor:
        pvm = sm.find_permission_view_menu("menu_access", menu_name)
        if pvm:
            sm.add_permission_role(rol_supervisor, pvm)

    # Crear usuario supervisor si no existe o asignarle el rol Supervisor
    user_supervisor = sm.find_user(username="supervisor")
    if not user_supervisor:
        sm.add_user(
            username="supervisor",
            first_name="Supervisor",
            last_name="General",
            email="supervisor@shoppingpc.com",
            role=rol_supervisor,
            password="supervisor123"
        )
    else:
        if rol_supervisor not in user_supervisor.roles:
            user_supervisor.roles.append(rol_supervisor)

    # --- Usuario ----------------------------------------------------
    rol_usuario = sm.find_role("Usuario") or sm.add_role("Usuario")

    vistas_usuario = ["ProductoView", "ClienteView", "VentaView", "DetalleVentaView"]
    for vista in vistas_usuario:
        for permiso in ["can_list", "can_show", "can_add"]:
            pvm = sm.find_permission_view_menu(permiso, vista)
            if pvm:
                sm.add_permission_role(rol_usuario, pvm)

    # Menús autorizados para Usuario
    menus_usuario = [
        "Catálogo", "Productos",
        "Ventas", "Clientes", "Ventas"
    ]
    for menu_name in menus_usuario:
        pvm = sm.find_permission_view_menu("menu_access", menu_name)
        if pvm:
            sm.add_permission_role(rol_usuario, pvm)

    from flask import current_app
    from app import db
    db.session.commit()
