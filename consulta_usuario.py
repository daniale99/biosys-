import flet as ft 
import airtable as at

def main(page:ft.Page):
    # Configuracion de la pagina
    page.title = "Consultas"
    page.theme_mode = "light"
    page.window.width = 800
    page.window.height = 600
    page.appbar = ft.AppBar(
        title=ft.Text("Consulta de usuarios en la nube"),
        leading=ft.Icon("CLOUD"),
        center_title=True,
        bgcolor="blue",
        color="white"
    )
    #Tabla de usuarios
    encabezado=[
        ft.DataColumn(ft.Text("Clave")),
        ft.DataColumn(ft.Text("Contraseña",)),
        ft.DataColumn(ft.Text("Nombre completo")),
        ft.DataColumn(ft.Text("Es administrador"))
    ]
    filas = []
    datos = at.Usuario.all()
    for d in datos: 
        celda1 = ft.DataCell(ft.Text(d.clave))
        celda2 = ft.DataCell(ft.Text(d.contra, color="white", selectable=True))
        celda3 = ft.DataCell(ft.Text(d.nombre))
        celda4 = ft.DataCell(ft.Text(d.admin))
        fila = ft.DataRow([celda1, celda2, celda3, celda4])
        filas.append(fila)

    tbl_usuarios = ft.DataTable(encabezado, filas)

    page.add(tbl_usuarios)
    page.update()






ft.app(target=main)