import flet as ft
from pyairtable import Table
from pyairtable.formulas import match

# Configura tus datos de Airtable aquí
API_KEY = "pattLhdx847VGiQFf.bcc6c3a471647d426987a63d5b932102fe59e34e331cbe0b2ebc1443873d0b1f"
BASE_ID = "appm3pqt6YX7RBfNf"
TABLE_NAME = "Usuario"  # Nombra tu tabla exacta

def main(page: ft.Page):
    # Inicializar tabla de airtable
    at = Table(API_KEY, BASE_ID, TABLE_NAME)

    # Función para validar usuario en Airtable
    def validar_usuario(usuario, password):
        try:
            formula = match({"clave": usuario, "contra": password})
            registro = at.first(formula=formula)
            if registro:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error de Airtable: {e}")
            return False

    # Página para agregar nuevo usuario
    def pagina_agregar_usuario(e):
        page.clean()
        page.title = "Agregar Nuevo Usuario"
        page.appbar = ft.AppBar(
            title=ft.Text("Agregar Nuevo Usuario"),
            bgcolor="blue",
            leading=ft.IconButton(icon="arrow_back", on_click=lambda _: pagina_principal())
        )

        input_usuario = ft.TextField(label="Clave usuario")
        input_password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)

        def agregar_usuario(e):
            clave = input_usuario.value
            contra = input_password.value
            if clave and contra:
                try:
                    # Verificar si usuario existe
                    formula = match({"clave": clave})
                    existe = at.first(formula=formula)
                    if existe:
                        page.snack_bar = ft.SnackBar(ft.Text("Usuario ya existe"))
                        page.snack_bar.open = True
                        page.update()
                    else:
                        # Crear registro en airtable
                        at.create({"clave": clave, "contra": contra})
                        page.snack_bar = ft.SnackBar(ft.Text("Usuario agregado correctamente"))
                        page.snack_bar.open = True
                        page.update()
                        pagina_principal()
                except Exception as e:
                    page.snack_bar = ft.SnackBar(ft.Text(f"Error: {e}"))
                    page.snack_bar.open = True
                    page.update()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Por favor, llena todos los campos"))
                page.snack_bar.open = True
                page.update()

        btn_guardar = ft.ElevatedButton("Guardar Usuario", on_click=agregar_usuario)
        page.add(input_usuario, input_password, btn_guardar)
        page.update()

    # Página para consultar usuarios
    def pagina_consultar_usuarios(e):
        page.clean()
        page.title = "Consultar Usuarios"
        page.appbar = ft.AppBar(
            title=ft.Text("Consultar Usuarios"),
            bgcolor="blue",
            leading=ft.IconButton(icon="arrow_back", on_click=lambda _: pagina_principal())
        )

        try:
            registros = at.all()

            # --- MODIFICACIÓN: Crear el DataTable ---
            data_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Clave")),
                    ft.DataColumn(ft.Text("Contraseña")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(r['fields'].get('clave', ''))),
                            # No se recomienda mostrar la contraseña en texto plano,
                            # pero para el ejemplo, se hace así.
                            # Para producción, se debe omitir este campo.
                            ft.DataCell(ft.Text(r['fields'].get('contra', ''))),
                        ]
                    ) for r in registros
                ]
            )

            # Agregar el DataTable a la página
            page.add(data_table)

        except Exception as e:
            page.add(ft.Text(f"Error al cargar usuarios: {e}"))
        
        page.update()

    # Página principal
    def pagina_principal():
        page.clean()
        page.title = "Menu Principal"
        page.appbar = ft.AppBar(
            title=ft.Text("SISTEMA DE GESTION DE ENERGIAS"),
            leading=ft.Icon("energy_sevings_leaf"),
            color="white",
            bgcolor="blue"
        )
        
        # Enlazar los botones a las funciones con `on_click`
        btn_agregar = ft.ElevatedButton("Agregar Nuevo Usuario", on_click=pagina_agregar_usuario)
        btn_consultar = ft.ElevatedButton("Consultar Usuarios", on_click=pagina_consultar_usuarios)

        page.add(btn_agregar, btn_consultar)
        page.update()

    # Pantalla de login
    def pagina_login():
        page.clean()
        page.title = "Iniciar Sesión"
        page.appbar = ft.AppBar(title=ft.Text("Login"), bgcolor="blue")

        txt_usuario = ft.TextField(label="Usuario")
        txt_password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
        lbl_mensaje = ft.Text(value="", color="red")

        def btn_login_click(e):
            usuario = txt_usuario.value
            password = txt_password.value
            if not usuario or not password:
                lbl_mensaje.value = "Por favor, ingresa usuario y contraseña"
                page.update()
                return
            
            if validar_usuario(usuario, password):
                lbl_mensaje.value = "¡Inicio de sesión exitoso!"
                lbl_mensaje.color = "green"
                page.update()
                # Redirigir a la página principal después de validar
                pagina_principal()
            else:
                lbl_mensaje.value = "Usuario o contraseña incorrectos"
                lbl_mensaje.color = "red"
                page.update()

        btn_login = ft.ElevatedButton("Iniciar Sesión", on_click=btn_login_click)
        page.add(txt_usuario, txt_password, btn_login, lbl_mensaje)
        page.update()

    # Empieza mostrando la pantalla de login
    pagina_login()

if __name__ == "__main__":
    ft.app(target=main)

