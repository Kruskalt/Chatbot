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
    def build(self):
        # Creamos un botón que abrirá el cuadro de diálogo
        button = Button(text='Introducir Huella')
        button.bind(on_press=self.check_fingerprint_and_show)
        return button

    def check_fingerprint_and_show(self, instance):
        # Verificamos la huella digital
        if fp.check_fingerprint("src/SOCOFing/Altered/1__M_Right_little_finger_Zcut.BMP"):
            # Si la huella digital es correcta, mostramos el cuadro de diálogo
            self.show_message()
        else:
            # Si la huella digital no es correcta, mostramos un mensaje
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
