from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.lang import Builder
from kivy.core.window import Window 
import requests
BASE_URL = "http://127.0.0.1:8000"

Window.size = (400, 700)
class LoginScreen(MDScreen):
    def login(self):
        codigo = self.ids.codigo_field.text  # Obtener el texto del campo de código
        if codigo ==  requests.post(f"{BASE_URL}/verificar/{codigo}").text: # Validar el código (verificar) # Ejemplo simple de validación
            self.manager.current = 'mesa'
        else:
            self.ids.error_label.text = "Código incorrecto"

    def show_forgot_code_dialog(self):
        dialog = MDDialog(
            title="Recuperar Código",
            text="Por favor, contacta al administrador para recuperar tu código.",
            buttons=[
                MDFlatButton(
                    text="CERRAR",
                    on_release=lambda *args: dialog.dismiss()
                )
            ]
        )
        dialog.open()

class LoginApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        # Cargar archivo .kv
        Builder.load_file('loginapp.kv')
        return LoginScreen()

if __name__ == '__main__':
    LoginApp().run()