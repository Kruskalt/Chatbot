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

class MyPopup(Popup):
    def __init__(self, callback, **kwargs):
        super(MyPopup, self).__init__(**kwargs)
        self.callback = callback

        # Creamos un layout para contener los widgets
        layout = BoxLayout(orientation='vertical')
        
        self.message_label = Label(text="")
        layout.add_widget(self.message_label)

        # Creamos un campo de entrada de texto
        self.input_text = TextInput(multiline=False)
        layout.add_widget(self.input_text)

        # Creamos un botón para enviar el valor ingresado
        button = Button(text='Enviar')
        button.bind(on_press=self.send_input)
        layout.add_widget(button)

        # Añadimos el layout al contenido del cuadro de diálogo
        self.content = layout

    def send_input(self, instance):
        # Al hacer clic en el botón, se llama a esta función y se pasa el texto ingresado al callback
        res = ch.chatbot_response(self.input_text.text)
        self.callback(res)
        self.message_label.text = res

    def on_dismiss(self):
        # Sobreescribimos el comportamiento predeterminado de on_dismiss
        pass


class MyApp(App):
     def seleccionar_archivo(self,instance):
        archivo = filedialog.askopenfilename()
        if archivo:
         print("Archivo seleccionado:", archivo)
         self.archivo_seleccionado_label.text= archivo
        
       
     def build(self):   
        # Creamos un diseño de caja para organizar nuestros widgets
        layout = BoxLayout(orientation='vertical')
        self.archivo_seleccionado_label= Label(text="")
        
        button_archivo = Button(text='Seleccionar archivo', size_hint_y=None, height=50)
        button_archivo.bind(on_press=self.seleccionar_archivo)
        
        # Crear otro botón
        button_iniciar = Button(text="Iniciar", size_hint_y=None, height=50)
        button_iniciar.bind(on_press=self.check_fingerprint_and_show)

        # Agregar botones al diseño
        layout.add_widget(button_archivo)
        layout.add_widget(button_iniciar)
        layout.add_widget(self.archivo_seleccionado_label)

        return layout

     
            
     def check_fingerprint_and_show(self,instance):
        archivo =  self.archivo_seleccionado_label.text
        print("estoy aca",archivo)
        if self.archivo_seleccionado_label.text != "":
            
        # Verificamos la huella digital
            if fp.check_fingerprint(archivo):
                # Si la huella digital es correcta, mostramos el cuadro de diálogo
                self.show_message()
            else:
            # Si la huella digital no es correcta, mostramos un mensaje
                self.show_invalid_fingerprint_message()
        else:
            self.show_invalid_fingerprint_message()
     def show_message(self):
        # Creamos y mostramos el cuadro de diálogo
        popup = MyPopup(callback=self.handle_input)
        popup.open()

     def show_invalid_fingerprint_message(self):
        # Creamos y mostramos un cuadro de diálogo de error
        invalid_fingerprint_popup = Popup(title='Error', content=Label(text='Huella digital incorrecta'), size_hint=(None, None), size=(400, 200))
        invalid_fingerprint_popup.open()

     def handle_input(self, user_input):
        # Aquí puedes manejar el valor ingresado por el usuario
        print("Valor ingresado:", user_input)

if __name__ == '__main__':
    MyApp().run()
