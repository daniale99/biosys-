import flet as ft 
import airtable as at

def main(page: ft.Page):


    def guardar_usuario (e:ft.ControlEvent):
        clave= txt_clave.value
        contra=txt_contra.value
        contra2=txt_contra2.value
        nombre=txt_nombre.value

        # confi contraseña 

        if clave=="":
            snackbar=ft.SnackBar(ft.Text("introduce tu clave de usuario "),bgcolor="orange",show_close_icon=True)
            page.open(snackbar)
            return

        if contra=="":
            snackbar=ft.SnackBar(ft.Text("introduce tu contraseña"),bgcolor="yellow",show_close_icon=True)
            page.open(snackbar)
            return    

        if  nombre=="":
            snackbar=ft.SnackBar(ft.Text("escribe tu nombre"),bgcolor="red",show_close_icon=True)
            page.open(snackbar)
            return

        
            
            
         

        if contra!=contra2:
            snackbar=ft.SnackBar(ft.Text("contraseña incorrecta"),bgcolor="red",show_close_icon=True)
            page.open(snackbar)
            return

        nuevo=at.Usuario(
          clave=clave,
          contra=contra,
          nombre=nombre,
          admin=chk_admin.value
    

        )
        try:
         nuevo.save()
         snackbar=ft.SnackBar(ft.Text("usuario registrado"),bgcolor="blue",show_close_icon=True)
         page.open(snackbar)
        except Exception as error:
            snackbar=ft.SnackBar(ft.Text(error),bgcolor="red",show_close_icon=True)
            page.open(snackbar)


        
        
          
    #Configuracion de la pagina 
    page.title = "Altas"
    page.theme_mode = "ligh"
    page.window.width = 800
    page.window.height = 600
    page.appbar = ft.AppBar(
        title=ft.Text("Nuevo usuario"),
        leading=ft.Icon("person_add"),
        color="white",
        bgcolor="purple"
    )
    #Componentes de la pagina
    txt_clave = ft.TextField(label="Clave del usuario")
    txt_contra = ft.TextField(label="contraseña", password=True)
    txt_contra2 = ft.TextField(label="Confirmar contraseña", password=True)
    txt_nombre = ft.TextField(label="Nombre completo")
    chk_admin = ft.Checkbox(label="¿Es administrador?")
    btn_guardar = ft.FilledButton(
        text="Guardar",
        icon="save",
        on_click= guardar_usuario
    )
    btn_cancelar = ft.FilledButton(
        text="Cancelar",
        icon="Cancel"
    )
    fila = ft.Row(controls=[btn_guardar, btn_cancelar])
    
    #Aladir componentes a la pagina 
    page.add(txt_clave, txt_contra, txt_contra2, txt_nombre, chk_admin,fila)
    page.update()



    page.update()


ft.app(target=main)




