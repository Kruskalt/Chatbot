import kivy
kivy.require('2.1.0')  # Reemplaza con tu versión actual de Kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import chatbot as ch
import fingerprint as fp
import tkinter as tk
from tkinter import filedialog
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
import os

class ChatBotScreen(Popup):
    def __init__(self, callback, **kwargs):
        super(ChatBotScreen, self).__init__(**kwargs)
        self.title = "Chatbot"

        # Creamos un layout para contener los widgets
        layout = BoxLayout(orientation='vertical')
        
        self.mensajeChatbot_label = Label(text="¡Bienvenido, soy el Chatbot, aquí apareceran mis respuestas!")
        layout.add_widget(self.mensajeChatbot_label)

        # Creamos un campo de entrada de texto
        self.user_input_text = TextInput(multiline=False, hint_text="Ingresa tu consulta aquí")
        layout.add_widget(self.user_input_text)

        # Creamos un botón para enviar el valor ingresado
        button = Button(text='Enviar', size_hint_y=None, height=50)
        button.bind(on_press=self.send_input)
        layout.add_widget(button)

        # Añadimos el layout al contenido del cuadro de diálogo
        self.content = layout

    def send_input(self, instance):
        # Al hacer clic en el botón, se llama a esta función y se pasa el texto ingresado al callback
        res = ch.chatbot_response(self.user_input_text.text)
        self.callback(res)
        self.mensajeChatbot_label.text = res
        self.user_input_text.text = ""

    def on_dismiss(self):
        # Sobreescribimos el comportamiento predeterminado de on_dismiss
        pass


class LoginRegisterScreen(Popup):
    def __init__(self, callback, **kwargs):
        super(LoginRegisterScreen, self).__init__(**kwargs)
        self.callback = callback
        self.title = "Inicio de sesión"

        layout = BoxLayout(orientation='vertical', spacing=10)

        title_label = Label(text="Bienvenido al Chatbot de League of Legends!", font_size=20)
        layout.add_widget(title_label)

        instruction_label = Label(text="Por favor, seleccione una opción:", font_size=16)
        layout.add_widget(instruction_label)

        button_login = Button(text="Iniciar Sesión", size_hint_y=None, height=50)
        button_login.bind(on_press=self.login)
        layout.add_widget(button_login)

        button_register = Button(text="Registrar Huella", size_hint_y=None, height=50)
        button_register.bind(on_press=self.register_fingerprint)
        layout.add_widget(button_register)

        self.content = layout

    def login(self, instance):
        direccion_huella = filedialog.askopenfilename()
        if direccion_huella:
            if fp.check_fingerprint(direccion_huella):
                self.callback()  # Llama a la función de callback al iniciar sesión correctamente
            else:
                invalid_fingerprint_popup = Popup(title='Error', content=Label(text='Huella digital incorrecta'), size_hint=(None, None), size=(400, 200))
                invalid_fingerprint_popup.open()

    def register_fingerprint(self, instance):
        direccion_huella = filedialog.askopenfilename()
        if direccion_huella:
            if fp.copiar_archivo_a_carpeta(direccion_huella):
                registro_cumplido_fingerprint_popup = Popup(title='Exito!', content=Label(text='Huella digital registrada correctamente'),
                                                             size_hint=(None, None), size=(400, 200))
                registro_cumplido_fingerprint_popup.open()
            else:
                invalid_fingerprint_popup = Popup(title='Error', content=Label(text='Huella digital ya registrada'), size_hint=(None, None), size=(400, 200))
                invalid_fingerprint_popup.open()


class ChatBot(App):
    def build(self):
        login_register_screen = LoginRegisterScreen(callback=self.open_chatbot_screen)
        login_register_screen.open()
        return BoxLayout()
    
    def open_chatbot_screen(self):
        ventana_chatbot = ChatBotScreen(callback= None)
        ventana_chatbot.open()

if __name__ == '__main__':
    ChatBot().run()

