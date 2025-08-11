import flet as ft
from pyairtable import Table
from typing import Optional

# --- CONFIG AIRTABLE ---
API_KEY = "pattLhdx847VGiQFf.bcc6c3a471647d426987a63d5b932102fe59e34e331cbe0b2ebc1443873d0b1f"
BASE_ID = "appm3pqt6YX7RBfNf"
TABLE_USUARIOS = "usuario"
TABLE_BIO = "bioenergia"

tabla_usuarios = Table(API_KEY, BASE_ID, TABLE_USUARIOS)
tabla_bio = Table(API_KEY, BASE_ID, TABLE_BIO)

V_OSCURO = "#4A148C"
V_PRINCIPAL = "#8E24AA"
V_CLARO = "#EDE7F6"
V_FOCO = "#6A1B9A"

def main(page: ft.Page):
    page.title = "Sistema de Gestión de Bioenergía de Tabasco"
    page.bgcolor = V_CLARO
    page.theme_mode = "light"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 24
    page.views.clear()
    page.window_width = 900
    page.window_height = 700

    # ---------- UTIL ----------
    def mostrar_snack(mensaje: str, color: str = V_FOCO):
        page.snack_bar = ft.SnackBar(ft.Text(mensaje), bgcolor=color, open=True)
        page.update()

    def safe_float(val: Optional[str], default: float = 0.0) -> Optional[float]:
        if val is None or str(val).strip() == "":
            return default
        try:
            return float(val)
        except Exception:
            return None

    # ---------- LOGIN (Airtable) ----------
    txt_login_clave = ft.TextField(label="Usuario (clave)", width=320)
    txt_login_contra = ft.TextField(label="Contraseña (contra)", password=True, can_reveal_password=True, width=320)

    logged_user = {"record": None}

    def do_login(e):
        clave = txt_login_clave.value.strip()
        contra = txt_login_contra.value.strip()
        if not clave or not contra:
            mostrar_snack("Ingresa usuario y contraseña.", color="blue")
            return

        try:
            # Buscar usuario en Airtable
            records = tabla_usuarios.all()
            found = None
            for r in records:
                f = r.get("fields", {})
                if str(f.get("clave", "")).strip() == clave and str(f.get("contra", "")).strip() == contra:
                    found = (r["id"], f)
                    break
            if not found:
                mostrar_snack("Usuario o contraseña incorrectos.", color="blue")
                return
            # login ok
            logged_user["record"] = found
            mostrar_snack(f"Bienvenido {found[1].get('nombre','')}", color=V_FOCO)
            page.go("/menu")
        except Exception as ex:
            mostrar_snack(f"Error login: {ex}", color="blue")

    # ---------- CAMPOS AGREGAR USUARIO ----------
    usuario_nombre = ft.TextField(label="Nombre", width=320)
    usuario_clave = ft.TextField(label="Clave", width=200)
    usuario_contra = ft.TextField(label="Contraseña", width=200)
    usuario_admin = ft.Checkbox(label="Admin")

    def agregar_usuario(e):
        if not usuario_nombre.value or not usuario_clave.value:
            mostrar_snack("Nombre y clave son obligatorios.", color="blue")
            return
        try:
            tabla_usuarios.create({
                "nombre": usuario_nombre.value,
                "clave": usuario_clave.value,
                "contra": usuario_contra.value,
                "admin": usuario_admin.value
            })
            mostrar_snack("Usuario agregado.", color=red)
            usuario_nombre.value = usuario_clave.value = usuario_contra.value = ""
            usuario_admin.value = False
            page.update()
            # refrescar lista si está visible
            if page.route == "/consultar-usuarios":
                consultar_usuarios_view.on_mount(None)
        except Exception as ex:
            mostrar_snack(f"Error agregando usuario: {ex}", color="#c62828")

    # ---------- CAMPOS AGREGAR BIOENERGIA ----------
    dd_cultivo = ft.Dropdown(label="Cultivo origen", width=320,
                             options=[ft.dropdown.Option(x) for x in ["Caña de azúcar", "Cacao", "Maíz", "Coco", "Plátano"]])
    dd_parte = ft.Dropdown(label="Parte aprovechada", width=320,
                           options=[ft.dropdown.Option(x) for x in ["Hoja", "Tallo", "Cáscara", "Bagazo", "Rastrojo"]])
    txt_municipio = ft.TextField(label="Municipio", width=320)
    txt_latitud = ft.TextField(label="Latitud", width=150)
    txt_longitud = ft.TextField(label="Longitud", width=150)
    txt_cantidad = ft.TextField(label="Cantidad (ton)", width=150)
    txt_area = ft.TextField(label="Área cultivada", width=150)
    txt_energia = ft.TextField(label="Contenido energético", width=150)

    def agregar_bio(e):
        # validaciones
        if not dd_cultivo.value or not dd_parte.value or not txt_municipio.value.strip():
            mostrar_snack("Completa cultivo, parte y municipio.", color="blue")
            return
        lat = safe_float(txt_latitud.value)
        lon = safe_float(txt_longitud.value)
        cant = safe_float(txt_cantidad.value)
        area = safe_float(txt_area.value)
        ener = safe_float(txt_energia.value)
        if lat is None or lon is None or cant is None or area is None or ener is None:
            mostrar_snack("Asegúrate que lat/lon/cantidad/area/energia sean números válidos.", color="blue")
            return
        try:
            tabla_bio.create({
                "cultivo": dd_cultivo.value,
                "parte": dd_parte.value,
                "municipio": txt_municipio.value.strip(),
                "latitud": lat,
                "longitud": lon,
                "cantidad": cant,
                "area": area,
                "energia": ener
            })
            mostrar_snack("Bioenergía registrada.", color=V_FOCO)
            # limpiar
            for c in [dd_cultivo, dd_parte, txt_municipio, txt_latitud, txt_longitud, txt_cantidad, txt_area, txt_energia]:
                if hasattr(c, "value"):
                    c.value = ""
            page.update()
            if page.route == "/consultar-biomasa":
                consultar_biomasa_view.on_mount(None)
        except Exception as ex:
            mostrar_snack(f"Error guardando bioenergía: {ex}", color="blue")

    # ---------- TABLAS / LISTADOS ----------
    tabla_bio_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Cultivo")),
            ft.DataColumn(ft.Text("Parte")),
            ft.DataColumn(ft.Text("Municipio")),
            ft.DataColumn(ft.Text("Cantidad (ton)")),
            ft.DataColumn(ft.Text("Área")),
            ft.DataColumn(ft.Text("Energía")),
            ft.DataColumn(ft.Text("Latitud")),
            ft.DataColumn(ft.Text("Longitud")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )

    tabla_usuarios_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Clave")),
            ft.DataColumn(ft.Text("Admin")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )

    def cargar_bio_table():
        try:
            records = tabla_bio.all()
            rows = []
            for r in records:
                f = r.get("fields", {})
                rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(f.get("cultivo", "")))),
                    ft.DataCell(ft.Text(str(f.get("parte", "")))),
                    ft.DataCell(ft.Text(str(f.get("municipio", "")))),
                    ft.DataCell(ft.Text(str(f.get("cantidad", "")))),
                    ft.DataCell(ft.Text(str(f.get("area", "")))),
                    ft.DataCell(ft.Text(str(f.get("energia", "")))),
                    ft.DataCell(ft.Text(str(f.get("latitud", "")))),
                    ft.DataCell(ft.Text(str(f.get("longitud", "")))),
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Eliminar",
                                          on_click=lambda e, _id=r["id"]: eliminar_bio(e, _id)),
                        ], spacing=5)
                    ),
                ]))
            tabla_bio_table.rows = rows
            page.update()
        except Exception as ex:
            mostrar_snack(f"Error cargando bioenergías: {ex}", color="blue")

    def cargar_usuarios_table():
        try:
            records = tabla_usuarios.all()
            rows = []
            for r in records:
                f = r.get("fields", {})
                rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(f.get("nombre", "")))),
                    ft.DataCell(ft.Text(str(f.get("clave", "")))),
                    ft.DataCell(ft.Text("Sí" if f.get("admin") else "No")),
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Eliminar",
                                          on_click=lambda e, _id=r["id"]: eliminar_usuario(e, _id)),
                        ], spacing=5)
                    ),
                ]))
            tabla_usuarios_table.rows = rows
            page.update()
        except Exception as ex:
            mostrar_snack(f"Error cargando usuarios: {ex}", color="blue")

    # ---------- ELIMINAR ----------
    def eliminar_bio(e, record_id):
        try:
            tabla_bio.delete(record_id)
            mostrar_snack("Registro de bioenergía eliminado.", color=V_FOCO)
            cargar_bio_table()
        except Exception as ex:
            mostrar_snack(f"Error eliminando: {ex}", color="blue")

    def eliminar_usuario(e, record_id):
        try:
            tabla_usuarios.delete(record_id)
            mostrar_snack("Usuario eliminado.", color=V_FOCO)
            cargar_usuarios_table()
        except Exception as ex:
            mostrar_snack(f"Error eliminando usuario: {ex}", color="blue")

    # ---------- VISTAS ----------
    def go_to(e, path): page.go(path)
    def go_back(e): page.go("/menu")

    # LOGIN VIEW
    login_view = ft.View(
        "/",
        controls=[
            ft.AppBar(title=ft.Text("Inicio de Sesión"), bgcolor=V_OSCURO),
            ft.Column([
                ft.Container(ft.Text("SISTEMA DE BIOENERGÍA - TABASCO", size=20, weight="bold", color=V_OSCURO), alignment=ft.alignment.center),
                ft.Container(height=12),
                txt_login_clave,
                txt_login_contra,
                ft.ElevatedButton("INICIAR SESIÓN", icon=ft.Icons.LOGIN, on_click=do_login,
                                  style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), bgcolor=V_FOCO, width=320),
                ft.Container(height=10),
                ft.Text("Credenciales de prueba: demo/demo o admin/admin", size=12, color="red")
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ]
    )

    # MAIN MENU VIEW
    main_menu_view = ft.View(
        "/menu",
        controls=[
            ft.AppBar(title=ft.Text("Menú Principal"), bgcolor=V_OSCURO),
            ft.Column([
                ft.Text("Menú Principal", size=28, weight="bold", color=V_OSCURO),
                ft.Divider(color=V_FOCO),
                ft.Row([
                    ft.ElevatedButton(
                        content=ft.Column([ft.Icon(name=ft.Icons.ADD_CIRCLE_OUTLINE, size=42, color="white"), ft.Text("Agregar Biomasa", color="white")],
                                          alignment=ft.MainAxisAlignment.CENTER),
                        on_click=lambda e: go_to(e, "/agregar-biomasa"),
                        width=180, height=140, bgcolor=V_PRINCIPAL,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=14))
                    ),
                    ft.ElevatedButton(
                        content=ft.Column([ft.Icon(name=ft.Icons.SEARCH, size=42, color="white"), ft.Text("Consultar Biomasa", color="white")],
                                          alignment=ft.MainAxisAlignment.CENTER),
                        on_click=lambda e: go_to(e, "/consultar-biomasa"),
                        width=180, height=140, bgcolor=V_PRINCIPAL,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=14))
                    ),
                    ft.ElevatedButton(
                        content=ft.Column([ft.Icon(name=ft.Icons.PERSON_ADD, size=42, color="white"), ft.Text("Agregar Usuario", color="white")],
                                          alignment=ft.MainAxisAlignment.CENTER),
                        on_click=lambda e: go_to(e, "/agregar-usuario"),
                        width=180, height=140, bgcolor=V_PRINCIPAL,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=14))
                    ),
                    ft.ElevatedButton(
                        content=ft.Column([ft.Icon(name=ft.Icons.PEOPLE, size=42, color="white"), ft.Text("Consultar Usuarios", color="white")],
                                          alignment=ft.MainAxisAlignment.CENTER),
                        on_click=lambda e: go_to(e, "/consultar-usuarios"),
                        width=180, height=140, bgcolor=V_PRINCIPAL,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=14))
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=18),
                ft.Container(height=14),
                ft.TextButton("Cerrar sesión", on_click=lambda e: page.go("/"), style=ft.ButtonStyle(color=V_FOCO))
            ], spacing=12, alignment=ft.MainAxisAlignment.CENTER)
        ]
    )

    # AGREGAR BIOMASA VIEW
    agregar_biomasa_view = ft.View(
        "/agregar-biomasa",
        controls=[
            ft.AppBar(title=ft.Text("Agregar Bioenergía"), bgcolor=V_OSCURO, leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=go_back)),
            ft.Column([
                ft.Text("Registro de Bioenergía", size=22, weight="bold", color=V_OSCURO),
                ft.Divider(color=V_FOCO),
                dd_cultivo, dd_parte, txt_municipio,
                ft.Row([txt_latitud, txt_longitud], spacing=16),
                ft.Row([txt_cantidad, txt_area], spacing=16),
                ft.Row([txt_energia], spacing=16),
                ft.Container(height=8),
                ft.ElevatedButton("GUARDAR DATOS", on_click=agregar_bio, width=320, bgcolor=V_FOCO, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
            ], spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ]
    )

    # CONSULTAR BIOMASA VIEW
    consultar_biomasa_view = ft.View(
        "/consultar-biomasa",
        controls=[
            ft.AppBar(title=ft.Text("Consultar Bioenergía"), bgcolor=V_OSCURO, leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=go_back)),
            ft.Column([
                ft.Text("Bioenergías Registradas", size=22, weight="bold", color=V_OSCURO),
                ft.Divider(color=V_FOCO),
                ft.Container(content=tabla_bio_table, width=860, height=420, bgcolor="white", padding=12, border_radius=8)
            ], spacing=12)
        ]
    )
    # actualizar cuando se muestre
    consultar_biomasa_view.on_mount = lambda e: cargar_bio_table()

    # AGREGAR USUARIO VIEW
    agregar_usuario_view = ft.View(
        "/agregar-usuario",
        controls=[
            ft.AppBar(title=ft.Text("Agregar Usuario"), bgcolor=V_OSCURO, leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=go_back)),
            ft.Column([
                ft.Text("Nuevo Usuario", size=22, weight="bold", color=V_OSCURO),
                ft.Divider(color=V_FOCO),
                usuario_nombre, ft.Row([usuario_clave, usuario_contra], spacing=12), usuario_admin,
                ft.Container(height=8),
                ft.ElevatedButton("GUARDAR USUARIO", on_click=agregar_usuario, width=320, bgcolor=V_FOCO, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
            ], spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ]
    )

    # CONSULTAR USUARIOS VIEW
    consultar_usuarios_view = ft.View(
        "/consultar-usuarios",
        controls=[
            ft.AppBar(title=ft.Text("Consultar Usuarios"), bgcolor=V_OSCURO, leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=go_back)),
            ft.Column([
                ft.Text("Usuarios", size=22, weight="bold", color=V_OSCURO),
                ft.Divider(color=V_FOCO),
                ft.Container(content=tabla_usuarios_table, width=600, height=420, bgcolor="white", padding=12, border_radius=8)
            ], spacing=12)
        ]
    )
    consultar_usuarios_view.on_mount = lambda e: cargar_usuarios_table()

    # ---------- ROUTING ----------
    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(login_view)
        elif page.route == "/menu":
            page.views.append(main_menu_view)
        elif page.route == "/agregar-biomasa":
            page.views.append(agregar_biomasa_view)
        elif page.route == "/consultar-biomasa":
            page.views.append(consultar_biomasa_view)
        elif page.route == "/agregar-usuario":
            page.views.append(agregar_usuario_view)
        elif page.route == "/consultar-usuarios":
            page.views.append(consultar_usuarios_view)
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

#Inicio de la aplicacion 
if __name__=="__main__":
     ft.app(target=main)







