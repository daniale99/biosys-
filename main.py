import flet as ft
import principal as pr

#Funcion principal
def main(page: ft.Page):

    def ingresar(e: ft.ControlEvent):
        page.clean()
        pr.main(page)

    #Configuracion de la página 
    page.theme_mode = "light"
    page.horizontal_alignment = "center"
    page.title= "inicio de sesion"
    page.window.width=800
    page.window.height=600

    #Componentes de la Página 
    logo = ft.Icon("person",size=100,color="pink")
    txt_bienvenido=ft.Text("bienvenido")
    txt_usuario=ft.TextField(label="username/correo",width=250)
    txt_contra= ft.TextField(label="contraseña",password=True,can_reveal_password=True,width=250)
    btn_login= ft.FilledButton(
        "iniciar sesion",
        icon=ft.Icons.LOGIN,
        width=300,
        color="white",
        bgcolor="pink",
        on_click=ingresar
        )

    page.add(logo,txt_bienvenido,txt_usuario,txt_contra,btn_login)
    #Actualizar la página 
    page.update()
#Inicio de la aplicacion 
if __name__=="__main__":
     ft.app(target=main, view=ft.AppView.WEB_BROWSER)
