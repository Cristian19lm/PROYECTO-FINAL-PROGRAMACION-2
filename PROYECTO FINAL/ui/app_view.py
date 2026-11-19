import flet as ft
from datetime import datetime
from data.database_manager import DatabaseManager
from data.cliente_dao import ClienteDAO
from data.producto_repository import ProductoRepository
from domain.cliente import Cliente
from domain.producto import Producto
from domain.venta import Venta

def main_view(page: ft.Page):
    page.title = "TechStore Manager - Sistema de Cómputo"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20
    page.theme_mode = ft.ThemeMode.DARK

    db = DatabaseManager()
    cliente_dao = ClienteDAO(db)
    producto_repo = ProductoRepository(db)

    tabla_clientes = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Nombre")),
        ft.DataColumn(ft.Text("Teléfono")),
        ft.DataColumn(ft.Text("Email")),
    ], rows=[])

    tabla_productos = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Nombre")),
        ft.DataColumn(ft.Text("Categoría")),
        ft.DataColumn(ft.Text("Precio")),
        ft.DataColumn(ft.Text("Stock")),
    ], rows=[])

    tabla_ventas = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("ID Venta")),
        ft.DataColumn(ft.Text("ID Cliente")),
        ft.DataColumn(ft.Text("ID Producto")),
        ft.DataColumn(ft.Text("Cant")),
        ft.DataColumn(ft.Text("Fecha")),
        ft.DataColumn(ft.Text("Total")),
    ], rows=[])

    def cargar_datos():
        tabla_clientes.rows.clear()
        for c in cliente_dao.obtener_todos():
            tabla_clientes.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(c.id_cliente))),
                ft.DataCell(ft.Text(c.nombre)),
                ft.DataCell(ft.Text(c.telefono)),
                ft.DataCell(ft.Text(c.email)),
            ]))
        
        tabla_productos.rows.clear()
        for p in producto_repo.obtener_productos():
            tabla_productos.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(p.id_producto))),
                ft.DataCell(ft.Text(p.nombre)),
                ft.DataCell(ft.Text(p.categoria)),
                ft.DataCell(ft.Text(f"${p.precio:,.2f}")),
                ft.DataCell(ft.Text(str(p.stock))),
            ]))

        tabla_ventas.rows.clear()
        for v in producto_repo.obtener_ventas():
            tabla_ventas.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(v.id_venta))),
                ft.DataCell(ft.Text(str(v.id_cliente))),
                ft.DataCell(ft.Text(str(v.id_producto))),
                ft.DataCell(ft.Text(str(v.cantidad))),
                ft.DataCell(ft.Text(v.fecha)),
                ft.DataCell(ft.Text(f"${v.total:,.2f}")),
            ]))
        page.update()

    # --- CAMPOS CLIENTES ---
    txt_cli_nombre = ft.TextField(label="Nombre Completo", width=300)
    txt_cli_tel = ft.TextField(label="Teléfono", width=200)
    txt_cli_email = ft.TextField(label="Correo Electrónico", width=300)

    def guardar_cliente(e):
        if not txt_cli_nombre.value or not txt_cli_tel.value:
            page.snack_bar = ft.SnackBar(ft.Text("Complete los campos obligatorios del cliente"))
            page.snack_bar.open = True
            page.update()
            return
        cli = Cliente(None, txt_cli_nombre.value, txt_cli_tel.value, txt_cli_email.value)
        cliente_dao.insertar(cli)
        txt_cli_nombre.value = ""
        txt_cli_tel.value = ""
        txt_cli_email.value = ""
        cargar_datos()
        page.snack_bar = ft.SnackBar(ft.Text("Cliente registrado exitosamente"))
        page.snack_bar.open = True
        page.update()

    btn_guardar_cli = ft.Button("Guardar Cliente", on_click=guardar_cliente, icon=ft.Icons.SAVE)

    # --- CAMPOS PRODUCTOS ---
    txt_prod_nombre = ft.TextField(label="Nombre del Producto", width=300)
    dd_prod_cat = ft.Dropdown(
        label="Categoría",
        width=250,
        options=[
            ft.dropdown.Option("Computador"),
            ft.dropdown.Option("Impresora"),
            ft.dropdown.Option("Mouse Inalámbrico"),
            ft.dropdown.Option("Celular"),
        ]
    )
    txt_prod_precio = ft.TextField(label="Precio Unitario ($)", width=150, keyboard_type=ft.KeyboardType.NUMBER)
    txt_prod_stock = ft.TextField(label="Stock Inicial", width=120, keyboard_type=ft.KeyboardType.NUMBER)

    def guardar_producto(e):
        try:
            prod = Producto(
                None,
                txt_prod_nombre.value,
                dd_prod_cat.value,
                float(txt_prod_precio.value),
                int(txt_prod_stock.value)
            )
            producto_repo.insertar_producto(prod)
            txt_prod_nombre.value = ""
            txt_prod_precio.value = ""
            txt_prod_stock.value = ""
            cargar_datos()
            page.snack_bar = ft.SnackBar(ft.Text("Producto registrado exitosamente"))
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al registrar producto: {ex}"))
            page.snack_bar.open = True
            page.update()

    btn_guardar_prod = ft.Button("Guardar Producto", on_click=guardar_producto, icon=ft.Icons.ADD_SHOPPING_CART)

    # --- CAMPOS VENTAS ---
    txt_venta_id_cli = ft.TextField(label="ID Cliente", width=120, keyboard_type=ft.KeyboardType.NUMBER)
    txt_venta_id_prod = ft.TextField(label="ID Producto", width=120, keyboard_type=ft.KeyboardType.NUMBER)
    txt_venta_cant = ft.TextField(label="Cantidad", width=100, keyboard_type=ft.KeyboardType.NUMBER)

    def realizar_venta(e):
        try:
            id_c = int(txt_venta_id_cli.value)
            id_p = int(txt_venta_id_prod.value)
            cant = int(txt_venta_cant.value)

            prods = producto_repo.obtener_productos()
            prod_encontrado = next((p for p in prods if p.id_producto == id_p), None)
            if not prod_encontrado:
                raise Exception("Producto no encontrado.")

            total = prod_encontrado.precio * cant
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            venta = Venta(None, id_c, id_p, cant, fecha_actual, total)
            exito = producto_repo.registrar_venta(venta)

            if exito:
                cargar_datos()
                page.snack_bar = ft.SnackBar(ft.Text(f"¡Venta realizada con éxito! Total: ${total:,.2f}"))
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Error: Stock insuficiente para completar la venta."))
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error en la venta: {ex}"))
            page.snack_bar.open = True
            page.update()

    btn_vender = ft.Button("Procesar Venta", on_click=realizar_venta, icon=ft.Icons.POINT_OF_SALE)

    # Contenedores para cada sección
    seccion_clientes = ft.Column([
        ft.Text("Registro de Clientes", size=20, weight=ft.FontWeight.BOLD),
        ft.Row([txt_cli_nombre, txt_cli_tel, txt_cli_email]),
        btn_guardar_cli,
        ft.Divider(),
        ft.Text("Lista de Clientes Registrados", size=16, weight=ft.FontWeight.BOLD),
        tabla_clientes
    ], scroll=ft.ScrollMode.AUTO, visible=True)

    seccion_productos = ft.Column([
        ft.Text("Gestión de Cómputo, Impresoras, Mouse y Celulares", size=20, weight=ft.FontWeight.BOLD),
        ft.Row([txt_prod_nombre, dd_prod_cat, txt_prod_precio, txt_prod_stock]),
        btn_guardar_prod,
        ft.Divider(),
        ft.Text("Inventario Actual", size=16, weight=ft.FontWeight.BOLD),
        tabla_productos
    ], scroll=ft.ScrollMode.AUTO, visible=False)

    seccion_ventas = ft.Column([
        ft.Text("Módulo de Ventas y Facturación", size=20, weight=ft.FontWeight.BOLD),
        ft.Row([txt_venta_id_cli, txt_venta_id_prod, txt_venta_cant]),
        btn_vender,
        ft.Divider(),
        ft.Text("Historial de Ventas", size=16, weight=ft.FontWeight.BOLD),
        tabla_ventas
    ], scroll=ft.ScrollMode.AUTO, visible=False)

    def cambiar_seccion(e):
        idx = e.control.selected_index
        seccion_clientes.visible = (idx == 0)
        seccion_productos.visible = (idx == 1)
        seccion_ventas.visible = (idx == 2)
        page.update()

    navegacion = ft.NavigationBar(
        selected_index=0,
        on_change=cambiar_seccion,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.PEOPLE, label="Clientes"),
            ft.NavigationBarDestination(icon=ft.Icons.COMPUTER, label="Inventario"),
            ft.NavigationBarDestination(icon=ft.Icons.POINT_OF_SALE, label="Ventas"),
        ]
    )

    page.add(
        ft.Text("TechStore - Sistema de Gestión Comercial", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
        navegacion,
        ft.Divider(),
        ft.Column([seccion_clientes, seccion_productos, seccion_ventas], expand=1)
    )
    cargar_datos()