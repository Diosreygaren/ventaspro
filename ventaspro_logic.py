import flet as ft
import datetime
import json

# Funciones de persistencia
def guardar_ventas(ventas_registradas):
    with open("ventas.json", "w") as f:
        json.dump(ventas_registradas, f)

def cargar_ventas():
    try:
        with open("ventas.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def guardar_notas(notas):
    with open("notas_vendedores.json", "w") as f:
        json.dump(notas, f)

def cargar_notas():
    try:
        with open("notas_vendedores.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def guardar_deudas(deudas):
    with open("deudas_clientes.json", "w") as f:
        json.dump(deudas, f)

def cargar_deudas():
    try:
        with open("deudas_clientes.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Funciones de validación y cálculo
def validar_campos_numericos(cantidad, precio_venta, precio_compra):
    try:
        cant = float(cantidad)
        if not cant.is_integer() or cant <= 0:
            return "La cantidad debe ser un número entero positivo."
        p_venta = float(precio_venta)
        if p_venta <= 0:
            return "El precio de venta debe ser un número positivo."
        p_compra = float(precio_compra)
        if p_compra <= 0:
            return "El precio de compra debe ser un número positivo."
        return None
    except ValueError:
        return "Los campos Cantidad, Precio de venta y Precio de compra deben ser numéricos."

def calcular_ganancia(cantidad, precio_venta, precio_compra, moneda_venta, moneda_compra, exchange_rate):
    cant = float(cantidad)
    p_venta = float(precio_venta) * (exchange_rate[0] if moneda_venta == "USD" else 1)
    p_compra = float(precio_compra) * (exchange_rate[0] if moneda_compra == "USD" else 1)
    return str((p_venta - p_compra) * cant)

# Función principal
def principal(page: ft.Page):
    page.title = "VentasProV1"
    page.window.icon = "logo.png"
    page.window.width = 600
    page.window.height = 700
    page.window_resizable = True
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = ft.Colors.GREY_200

    ventas_registradas = cargar_ventas()
    notas_vendedores = cargar_notas()
    deudas_clientes = cargar_deudas()
    exchange_rate = [62]

    def ajustar_tamano() -> tuple[int, int]:
        if page.window.width < 600:
            return 16, 10
        return 24, 20

    # Funciones de navegación
    def ir_a_inicio(e):
        page.go("/")

    def ir_a_ventas(e):
        page.go("/ventas")

    def ir_a_productos(e):
        page.go("/productos")

    def ir_a_vendedores(e):
        page.go("/vendedores")

    def ir_a_otra_funcion(e):
        page.go("/otra funcion")

    def eliminar_ultima_venta(e):
        if ventas_registradas:
            ventas_registradas.pop()
            guardar_ventas(ventas_registradas)
            page.go("/ventas")

    # Vista de Ventas
    def crear_formulario_venta():
        def calcular_ganancia_en_tiempo_real(e):
            try:
                cantidad = float(cantidad_de_articulos_a_vender.value)
                p_venta = float(precio_de_venta_final.value)
                if moneda_venta.value == "USD": p_venta *= exchange_rate[0]
                p_compra = float(precio_de_compra_inicial.value)
                if moneda_compra.value == "USD": p_compra *= exchange_rate[0]
                ganancia = (p_venta - p_compra) * cantidad
                campo_de_cuanto_se_le_ganara_a_la_venta.value = str(ganancia)
            except ValueError:
                campo_de_cuanto_se_le_ganara_a_la_venta.value = ""
            page.update()

        def registrar_venta(e):
            required_fields = [nombre_del_vendedor, articulo_a_vender, cantidad_de_articulos_a_vender,
                               precio_de_venta_final, precio_de_compra_inicial, nombre_de_cliente_a_vender,
                               posible_fecha_de_entrega]
            if any(field.value.strip() == "" for field in required_fields):
                mensaje_error.value = "Por favor, completa todos los campos requeridos."
                mensaje_error.color = ft.Colors.RED
                page.update()
                return

            error_numerico = validar_campos_numericos(cantidad_de_articulos_a_vender.value,
                                                      precio_de_venta_final.value, precio_de_compra_inicial.value)
            if error_numerico:
                mensaje_error.value = error_numerico
                mensaje_error.color = ft.Colors.RED
                page.update()
                return

            venta_data = {
                "vendedor": nombre_del_vendedor.value,
                "articulo": articulo_a_vender.value,
                "detalle": detalle.value,
                "cantidad": cantidad_de_articulos_a_vender.value,
                "precio_venta": precio_de_venta_final.value,
                "moneda_venta": moneda_venta.value,
                "precio_compra": precio_de_compra_inicial.value,
                "moneda_compra": moneda_compra.value,
                "cliente": nombre_de_cliente_a_vender.value,
                "observaciones": observaciones.value,
                "fecha": posible_fecha_de_entrega.value,
                "ganancia": campo_de_cuanto_se_le_ganara_a_la_venta.value,
                "prioridad": False,
                "reportada": False
            }
            if ventas_registradas and venta_data == ventas_registradas[-1]:
                mensaje_error.value = "Esta venta ya fue registrada. Modifica algún dato."
                mensaje_error.color = ft.Colors.RED
                page.update()
                return

            ventas_registradas.append(venta_data)
            guardar_ventas(ventas_registradas)
            mensaje_error.value = "Venta registrada con éxito."
            mensaje_error.color = ft.Colors.GREEN
            t.value = f"El vendedor: '{nombre_del_vendedor.value}' vende '{articulo_a_vender.value}' con ganancia '{campo_de_cuanto_se_le_ganara_a_la_venta.value}'."
            page.update()

        def hacer_otra_venta(e):
            for field in [nombre_del_vendedor, articulo_a_vender, detalle, cantidad_de_articulos_a_vender,
                          precio_de_venta_final, precio_de_compra_inicial, nombre_de_cliente_a_vender,
                          observaciones, campo_de_cuanto_se_le_ganara_a_la_venta]:
                field.value = ""
            posible_fecha_de_entrega.value = (datetime.datetime.now() + datetime.timedelta(days=5)).strftime("%d/%m/%Y")
            moneda_venta.value = "DOP"
            moneda_compra.value = "DOP"
            t.value = ""
            mensaje_error.value = ""
            page.update()

        t = ft.Text()
        mensaje_error = ft.Text("", size=16)
        nombre_del_vendedor = ft.TextField(hint_text="Nombre del vendedor", width=300, bgcolor=ft.Colors.WHITE)
        articulo_a_vender = ft.TextField(label="Artículo", width=300, bgcolor=ft.Colors.WHITE)
        detalle = ft.TextField(label="Detalle", width=300, bgcolor=ft.Colors.WHITE)
        cantidad_de_articulos_a_vender = ft.TextField(label="Cantidad", width=300, bgcolor=ft.Colors.WHITE)
        precio_de_venta_final = ft.TextField(label="Precio de venta", width=200, bgcolor=ft.Colors.WHITE)
        precio_de_compra_inicial = ft.TextField(label="Precio de compra", width=200, bgcolor=ft.Colors.WHITE)
        nombre_de_cliente_a_vender = ft.TextField(label="Nombre del cliente", width=300, bgcolor=ft.Colors.WHITE)
        observaciones = ft.TextField(label="Observaciones", width=300, bgcolor=ft.Colors.WHITE)
        posible_fecha_de_entrega = ft.TextField(
            label="Fecha de entrega",
            value=(datetime.datetime.now() + datetime.timedelta(days=5)).strftime("%d/%m/%Y"),
            width=300,
            bgcolor=ft.Colors.WHITE
        )
        campo_de_cuanto_se_le_ganara_a_la_venta = ft.TextField(
            label="Ganancia =",
            width=300,
            disabled=True,
            bgcolor=ft.Colors.WHITE
        )
        moneda_venta = ft.Dropdown(
            options=[ft.dropdown.Option("DOP"), ft.dropdown.Option("USD")],
            value="DOP",
            width=100
        )
        moneda_compra = ft.Dropdown(
            options=[ft.dropdown.Option("DOP"), ft.dropdown.Option("USD")],
            value="DOP",
            width=100
        )

        row_precio_venta = ft.Row(controls=[precio_de_venta_final, moneda_venta], spacing=10)
        row_precio_compra = ft.Row(controls=[precio_de_compra_inicial, moneda_compra], spacing=10)

        for field in [precio_de_venta_final, precio_de_compra_inicial, cantidad_de_articulos_a_vender,
                      moneda_venta, moneda_compra]:
            field.on_change = calcular_ganancia_en_tiempo_real

        lista = ft.ListTile(
            title=ft.Text("Opciones"),
            trailing=ft.PopupMenuButton(
                icon=ft.Icons.MORE_VERT,
                items=[
                    ft.PopupMenuItem(text="Hacer otra venta", on_click=hacer_otra_venta),
                    ft.PopupMenuItem(text="Darle prioridad", on_click=lambda e: print("Prioridad asignada")),
                ],
            ),
        )
        boton_registrar = ft.ElevatedButton(
            text="Registrar venta",
            on_click=registrar_venta,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.PURPLE_300
        )
        boton_volver = ft.ElevatedButton(
            "Volver",
            on_click=ir_a_inicio,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.PURPLE_300
        )

        formulario = ft.ListView(
            controls=[
                ft.Text("Registrar Venta", size=ajustar_tamano()[0], weight=ft.FontWeight.W_900,
                        color=ft.Colors.PURPLE_700),
                nombre_del_vendedor, articulo_a_vender, detalle, cantidad_de_articulos_a_vender,
                row_precio_venta, row_precio_compra, campo_de_cuanto_se_le_ganara_a_la_venta,
                nombre_de_cliente_a_vender, observaciones, posible_fecha_de_entrega, lista,
                boton_registrar, boton_volver, mensaje_error, t
            ],
            spacing=15,
            expand=True,
            auto_scroll=False
        )
        return formulario

    def vista_ventas():
        print("Cargando vista_ventas")
        container = ft.Container(
            content=crear_formulario_venta(),
            padding=ajustar_tamano()[1],
            bgcolor=ft.Colors.GREY_100,
            border_radius=15,
            expand=True
        )
        return ft.View("/ventas", controls=[container])

    # Vista de Productos (con borrado de ventas)
    def vista_productos():
        def alternar_modo_edicion(indice, container, detalles_venta, edit_controls):
            venta = ventas_registradas[indice]
            if container.content.controls[-1] == detalles_venta:
                container.content.controls[-1] = edit_controls
            else:
                nuevos_datos = {
                    "vendedor": venta["vendedor"], "articulo": edit_controls.controls[0].value,
                    "cantidad": edit_controls.controls[1].value, "precio_compra": edit_controls.controls[2].value,
                    "precio_venta": edit_controls.controls[3].value, "moneda_compra": edit_controls.controls[4].value,
                    "moneda_venta": edit_controls.controls[5].value, "cliente": edit_controls.controls[6].value,
                    "fecha": edit_controls.controls[7].value, "observaciones": edit_controls.controls[8].value,
                    "detalle": venta["detalle"], "prioridad": venta["prioridad"], "reportada": venta["reportada"]
                }
                error = validar_campos_numericos(nuevos_datos["cantidad"], nuevos_datos["precio_venta"],
                                                 nuevos_datos["precio_compra"])
                if error:
                    page.snack_bar = ft.SnackBar(ft.Text(error), bgcolor=ft.Colors.RED)
                    page.snack_bar.open = True
                    page.update()
                    return
                nuevos_datos["ganancia"] = calcular_ganancia(nuevos_datos["cantidad"], nuevos_datos["precio_venta"],
                                                             nuevos_datos["precio_compra"],
                                                             nuevos_datos["moneda_venta"],
                                                             nuevos_datos["moneda_compra"], exchange_rate)
                ventas_registradas[indice] = nuevos_datos
                guardar_ventas(ventas_registradas)
                nuevos_detalles = crear_detalles_venta(nuevos_datos, indice, container)
                nuevos_detalles.controls[-1].data = (indice, container, nuevos_detalles, edit_controls)
                container.content.controls[-1] = nuevos_detalles
            page.update()

        def dar_prioridad(indice):
            ventas_registradas[indice]["prioridad"] = True
            ventas_registradas[indice]["reportada"] = False
            guardar_ventas(ventas_registradas)
            page.update()

        def reportar_venta(indice):
            ventas_registradas[indice]["reportada"] = True
            ventas_registradas[indice]["prioridad"] = False
            guardar_ventas(ventas_registradas)
            page.update()

        def crear_edit_controls(venta, indice, container):
            controls = [
                ft.TextField(label="Artículo", value=venta["articulo"], width=200),
                ft.TextField(label="Cantidad", value=venta["cantidad"], width=200),
                ft.TextField(label="P. Compra", value=venta["precio_compra"], width=200),
                ft.TextField(label="P. Venta", value=venta["precio_venta"], width=200),
                ft.Dropdown(options=[ft.dropdown.Option("DOP"), ft.dropdown.Option("USD")],
                            value=venta["moneda_compra"], width=100),
                ft.Dropdown(options=[ft.dropdown.Option("DOP"), ft.dropdown.Option("USD")], value=venta["moneda_venta"],
                            width=100),
                ft.TextField(label="Cliente", value=venta["cliente"], width=200),
                ft.TextField(label="Fecha", value=venta["fecha"], width=200),
                ft.TextField(label="Observaciones", value=venta["observaciones"], width=200),
                ft.ElevatedButton("Guardar", on_click=lambda e: alternar_modo_edicion(*e.control.data),
                                  bgcolor=ft.Colors.PURPLE_300, color=ft.Colors.WHITE)
            ]
            return ft.Column(controls, spacing=5)

        def crear_detalles_venta(venta, indice, container):
            controls = [
                ft.Text(f"Artículo: {venta['articulo']}"),
                ft.Text(f"Cantidad: {venta['cantidad']}"),
                ft.Text(f"P. Compra: {venta['precio_compra']} {venta['moneda_compra']}"),
                ft.Text(f"P. Venta: {venta['precio_venta']} {venta['moneda_venta']}"),
                ft.Text(f"Ganancia: {venta['ganancia']}"),
                ft.Text(f"Cliente: {venta['cliente']}"),
                ft.Text(f"Fecha: {venta['fecha']}"),
                ft.Text(f"Obs: {venta['observaciones']}"),
                ft.Row([
                    ft.ElevatedButton("Editar", on_click=lambda e: alternar_modo_edicion(*e.control.data),
                                      bgcolor=ft.Colors.PURPLE_300, color=ft.Colors.WHITE),
                    ft.ElevatedButton("Prioridad", on_click=lambda e: dar_prioridad(indice),
                                      bgcolor=ft.Colors.YELLOW_700, color=ft.Colors.BLACK),
                    ft.ElevatedButton("Reportar", on_click=lambda e: reportar_venta(indice), bgcolor=ft.Colors.RED_300,
                                      color=ft.Colors.WHITE)
                ], spacing=5)
            ]
            return ft.Column(controls, spacing=5)

        def borrar_todas_ventas(e):
    def verificar_contraseña(e):
        try:
            password_entered = float(entrada_contraseña.value)
            if password_entered == exchange_rate[0]:
                ventas_registradas.clear()
                guardar_ventas(ventas_registradas)
                page.snack_bar = ft.SnackBar(
                    ft.Text("Todas las ventas han sido eliminadas exitosamente."),
                    bgcolor=ft.Colors.GREEN
                )
                page.snack_bar.open = True
                page.go("/productos")  # Refresca la vista
            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Contraseña incorrecta. Intente de nuevo."),
                    bgcolor=ft.Colors.RED
                )
                page.snack_bar.open = True
            page.dialog.open = False
            page.update()
        except ValueError:
            page.snack_bar = ft.SnackBar(
                ft.Text("Ingrese un número válido como contraseña."),
                bgcolor=ft.Colors.RED
            )
            page.snack_bar.open = True
            page.update()

    # Crear un diálogo para ingresar la contraseña
    entrada_contraseña = ft.TextField(
        label="Ingrese el cambio de divisa como contraseña",
        password=True,
        width=300
    )
    dialogo = ft.AlertDialog(
        title=ft.Text("Confirmar eliminación de todas las ventas", weight=ft.FontWeight.BOLD),
        content=ft.Column([
            ft.Text("Por seguridad, ingrese el valor actual del cambio de divisa (ejemplo: 60):"),
            entrada_contraseña
        ], spacing=10),
        actions=[
            ft.ElevatedButton(
                "Confirmar",
                on_click=verificar_contraseña,
                bgcolor=ft.Colors.PURPLE_300,
                color=ft.Colors.WHITE
            ),
            ft.ElevatedButton(
                "Cancelar",
                on_click=lambda e: setattr(page.dialog, 'open', False) or page.update(),
                bgcolor=ft.Colors.GREY_400,
                color=ft.Colors.WHITE
            )
        ]
    )
    page.dialog = dialogo
    dialogo.open = True
    page.update()
    
        ventas_por_vendedor = {}
        for indice, venta in enumerate(ventas_registradas):
            nombre_normalizado = venta["vendedor"].strip().lower()
            if nombre_normalizado not in ventas_por_vendedor:
                ventas_por_vendedor[nombre_normalizado] = {"nombre": venta["vendedor"].strip(), "ventas": []}
            ventas_por_vendedor[nombre_normalizado]["ventas"].append((venta, indice))

        contenedores_vendedores = []
        for key in sorted(ventas_por_vendedor.keys()):
            vendedor_info = ventas_por_vendedor[key]
            lista_ventas = []
            for venta, indice in vendedor_info["ventas"]:
                container_venta = ft.Container(
                    content=ft.Column([]),
                    padding=10,
                    bgcolor=ft.Colors.YELLOW_700 if venta["prioridad"] else ft.Colors.RED_300 if venta[
                        "reportada"] else ft.Colors.GREEN_100,
                    border_radius=5
                )
                detalles_venta = crear_detalles_venta(venta, indice, container_venta)
                edit_controls = crear_edit_controls(venta, indice, container_venta)
                detalles_venta.controls[-1].controls[0].data = (indice, container_venta, detalles_venta, edit_controls)
                edit_controls.controls[-1].data = (indice, container_venta, detalles_venta, edit_controls)
                container_venta.content.controls.append(detalles_venta)
                lista_ventas.append(container_venta)

            lista_ventas_view = ft.ListView(controls=lista_ventas, expand=True, auto_scroll=True, padding=10)
            contenedor_vendedor = ft.Container(
                content=ft.Column(
                    [ft.Text(f"Vendedor: {vendedor_info['nombre']}", weight=ft.FontWeight.BOLD), lista_ventas_view],
                    spacing=5),
                padding=10,
                bgcolor=ft.Colors.GREEN_50,
                border_radius=5,
                expand=True
            )
            contenedores_vendedores.append(contenedor_vendedor)

        grid_vendedores = ft.GridView(controls=contenedores_vendedores, max_extent=400, spacing=10, run_spacing=10,
                                      expand=True)
        list_tile_opciones = ft.ListTile(
            title=ft.Text("Opciones de Venta"),
            trailing=ft.PopupMenuButton(
                icon=ft.Icons.MORE_VERT,
                items=[
                    ft.PopupMenuItem(text="Agregar nueva venta", on_click=lambda e: page.go("/ventas")),
                    ft.PopupMenuItem(text="Eliminar última venta", on_click=eliminar_ultima_venta),
                    ft.PopupMenuItem(text="Borrar todas las ventas", on_click=borrar_todas_ventas)
                ],
            ),
        )
        boton_volver = ft.ElevatedButton("Volver", on_click=ir_a_inicio, bgcolor=ft.Colors.PURPLE_300,
                                         color=ft.Colors.WHITE)
        print("Cargando vista_productos")
        return ft.View("/productos", controls=[
            ft.Container(content=ft.Column([list_tile_opciones, grid_vendedores, boton_volver], spacing=10),
                         padding=ajustar_tamano()[1], bgcolor=ft.Colors.PURPLE_50, border_radius=15, expand=True)])

    # Vista de Inicio
    def vista_inicio():
        print("Cargando vista_inicio")
        fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")
        tamano_texto, padding = ajustar_tamano()

        botones = ft.Column(
            controls=[
                ft.ElevatedButton("Ir a Registrar Venta", width=200, on_click=ir_a_ventas, bgcolor=ft.Colors.PURPLE_300,
                                  color=ft.Colors.WHITE),
                ft.ElevatedButton("Administrador De Ventas", width=200, on_click=ir_a_productos,
                                  bgcolor=ft.Colors.PURPLE_300, color=ft.Colors.WHITE),
                ft.ElevatedButton("Divisa y Notas", width=200, on_click=ir_a_vendedores,
                                  bgcolor=ft.Colors.PURPLE_300, color=ft.Colors.WHITE),
                ft.ElevatedButton("Acerca de v1", width=200, on_click=ir_a_otra_funcion, bgcolor=ft.Colors.PURPLE_300,
                                  color=ft.Colors.WHITE)
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        content = ft.Column(
            controls=[
                ft.Text("Bienvenido al Sistema de Ventas", size=tamano_texto + 10, color=ft.Colors.WHITE,
                        weight=ft.FontWeight.BOLD),
                botones,
                ft.Text(f"El cambio de divisa es de {exchange_rate[0]}", size=tamano_texto, color=ft.Colors.WHITE),
                ft.Text(f"Fecha actual: {fecha_actual}", size=tamano_texto - 4, color=ft.Colors.WHITE)
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        container = ft.Container(
            content=content,
            padding=padding,
            bgcolor=ft.Colors.PURPLE_700,
            border_radius=15,
            expand=True
        )
        return ft.View("/", controls=[container])

    # Vista de Vendedores (con gestión de deudas)
    def vista_vendedores():
        def actualizar_divisa(e):
            try:
                exchange_rate[0] = float(cambio_divisa.value)
            except ValueError:
                print("Ingrese un valor numérico válido.")
            page.update()

        def agregar_nota(e):
            if campo_notas.value.strip():
                notas_vendedores.append(
                    {"fecha": datetime.datetime.now().strftime("%d/%m/%Y"), "texto": campo_notas.value})
                guardar_notas(notas_vendedores)
                lista_notas.controls.append(
                    ft.Text(f"{notas_vendedores[-1]['fecha']}: {notas_vendedores[-1]['texto']}"))
                campo_notas.value = ""
                page.update()

        def registrar_deuda(e):
            if not all([nombre_cliente.value, monto_deuda.value]):
                mensaje_error.value = "Falta nombre o monto."
                mensaje_error.color = ft.Colors.RED
                page.update()
                return
            try:
                monto = float(monto_deuda.value)
                if monto <= 0:
                    raise ValueError
            except ValueError:
                mensaje_error.value = "El monto debe ser un número positivo."
                mensaje_error.color = ft.Colors.RED
                page.update()
                return
            deuda = {
                "nombre": nombre_cliente.value,
                "monto_inicial": monto,
                "monto_actual": monto,
                "fecha_inicio": datetime.datetime.now().strftime("%d/%m/%Y"),
                "pagos": []
            }
            deudas_clientes.append(deuda)
            guardar_deudas(deudas_clientes)
            actualizar_lista_deudas()
            nombre_cliente.value = ""
            monto_deuda.value = ""
            mensaje_error.value = "Deuda registrada."
            mensaje_error.color = ft.Colors.GREEN
            page.update()

        def registrar_pago(indice):
            try:
                monto = float(campo_pago.value)
                if monto <= 0 or monto > deudas_clientes[indice]["monto_actual"]:
                    raise ValueError
            except ValueError:
                mensaje_error.value = "Monto inválido o mayor a la deuda."
                mensaje_error.color = ft.Colors.RED
                page.update()
                return
            deudas_clientes[indice]["monto_actual"] -= monto
            deudas_clientes[indice]["pagos"].append({
                "monto": monto,
                "fecha": datetime.datetime.now().strftime("%d/%m/%Y")
            })
            guardar_deudas(deudas_clientes)
            actualizar_lista_deudas()
            campo_pago.value = ""
            mensaje_error.value = "Pago registrado."
            mensaje_error.color = ft.Colors.GREEN
            page.update()

        def actualizar_lista_deudas():
            lista_deudas.controls.clear()
            for i, deuda in enumerate(deudas_clientes):
                texto_deuda = f"{deuda['nombre']} - Debe: {deuda['monto_actual']} (Inicio: {deuda['monto_inicial']} el {deuda['fecha_inicio']})"
                pagos_texto = ", ".join([f"{p['monto']} el {p['fecha']}" for p in deuda['pagos']]) if deuda['pagos'] else "Sin pagos"
                lista_deudas.controls.append(
                    ft.Row([
                        ft.Text(texto_deuda),
                        ft.Text(f"Pagos: {pagos_texto}"),
                        ft.ElevatedButton("Pagar", on_click=lambda e, idx=i: registrar_pago(idx))
                    ])
                )

        tamano_texto, padding = ajustar_tamano()
        cambio_divisa = ft.TextField(label="Cambio de Divisa", value=str(exchange_rate[0]), width=150, bgcolor=ft.Colors.WHITE)
        cambio_divisa.on_change = actualizar_divisa
        campo_notas = ft.TextField(label="Agregar nota", width=400, bgcolor=ft.Colors.WHITE)
        boton_agregar_nota = ft.ElevatedButton("Guardar Nota", on_click=agregar_nota, bgcolor=ft.Colors.PURPLE_300, color=ft.Colors.WHITE)
        lista_notas = ft.ListView(controls=[ft.Text(f"{nota['fecha']}: {nota['texto']}") for nota in notas_vendedores], expand=True, padding=10)
        nombre_cliente = ft.TextField(label="Nombre del cliente", width=200, bgcolor=ft.Colors.WHITE)
        monto_deuda = ft.TextField(label="Monto de la deuda", width=150, bgcolor=ft.Colors.WHITE)
        boton_registrar_deuda = ft.ElevatedButton("Registrar Deuda", on_click=registrar_deuda, bgcolor=ft.Colors.PURPLE_300, color=ft.Colors.WHITE)
        campo_pago = ft.TextField(label="Monto del pago", width=150, bgcolor=ft.Colors.WHITE)
        lista_deudas = ft.ListView(expand=True, padding=10)
        mensaje_error = ft.Text("", size=16)
        actualizar_lista_deudas()
        boton_volver = ft.ElevatedButton("Volver", on_click=ir_a_inicio, bgcolor=ft.Colors.PURPLE_300, color=ft.Colors.WHITE)

        return ft.View("/vendedores", controls=[ft.Container(
            content=ft.Column([
                ft.Text("Administrar Divisa, Notas y Deudas", size=tamano_texto, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
                cambio_divisa,
                campo_notas, boton_agregar_nota, lista_notas,
                ft.Text("Gestión de Deudas", size=tamano_texto - 2, weight=ft.FontWeight.BOLD),
                ft.Row([nombre_cliente, monto_deuda, boton_registrar_deuda]),
                ft.Row([campo_pago]),
                lista_deudas,
                mensaje_error, boton_volver
            ], spacing=15),
            padding=padding, bgcolor=ft.Colors.GREY_100, border_radius=15, expand=True
        )])

    # Vista Acerca de (mejorada)
    def vista_otra_funcion():
        tamano_texto, padding = ajustar_tamano()
        return ft.View("/otra funcion", controls=[ft.Container(
            content=ft.Column([
                ft.Text("Acerca de VentasPro", size=tamano_texto + 4, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700, text_align=ft.TextAlign.CENTER),
                ft.Text("Versión 1.0", size=tamano_texto - 2, color=ft.Colors.GREY_800, text_align=ft.TextAlign.CENTER),
                ft.Text("Gestión de ventas y deudas simplificada", size=tamano_texto - 4, color=ft.Colors.GREY_700, text_align=ft.TextAlign.CENTER),
                ft.Text("Desarrollado por Diego", size=tamano_texto - 2, color=ft.Colors.GREY_800, text_align=ft.TextAlign.CENTER),
                ft.Text("Contacto: soportesistema1414@gmail.com | +1 809-555-1234", size=tamano_texto - 6, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
                ft.Text("© 2025 DMAI - Todos los derechos reservados", size=tamano_texto - 8, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
                ft.ElevatedButton("Volver", on_click=ir_a_inicio, bgcolor=ft.Colors.PURPLE_300, color=ft.Colors.WHITE)
            ], spacing=20, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=padding, bgcolor=ft.Colors.PURPLE_50, border_radius=15, expand=True
        )])

    # Manejo de rutas
    def cambiar_de_ruta(e):
        print(f"Cambiando a ruta: {page.route}")
        page.views.clear()
        if page.route == "/":
            page.views.append(vista_inicio())
        elif page.route == "/ventas":
            page.views.append(vista_ventas())
        elif page.route == "/productos":
            page.views.append(vista_productos())
        elif page.route == "/vendedores":
            page.views.append(vista_vendedores())
        elif page.route == "/otra funcion":
            page.views.append(vista_otra_funcion())
        else:
            page.views.append(ft.View(page.route, controls=[ft.Text("Ruta no encontrada")]))
        page.update()

    page.on_route_change = cambiar_de_ruta
    print("Iniciando aplicación")
    page.go("/")
