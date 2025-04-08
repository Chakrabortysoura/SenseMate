import os
import requests
import datetime
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image as widget_image
from kivy.utils import platform
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

if platform == "android":
    from android.permissions import request_permissions, Permission
    from androidstorage4kivy import SharedStorage
    from jnius import autoclass

class SenseMate(App):

    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.8, 0.9)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # Robotic Background Theme
        self.window.canvas.before.clear()
        with self.window.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.05, 0.07, 0.1, 1)
            self.bg_rect = Rectangle(pos=self.window.pos, size=self.window.size)
            self.window.bind(pos=self.update_bg, size=self.update_bg)

        self.window.add_widget(widget_image(source="sensemate.png"))

        input_box = BoxLayout(
            orientation='vertical',
            size_hint=(0.9, None),
            height=60,
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            padding=[10, 10],
            spacing=5
        )

        self.txt_input = TextInput(
            hint_text="Enter IP address of the ESP",
            size_hint=(1, 1),
            font_size='18sp',
            halign="center",
            background_color=[1, 1, 1, 1],
            foreground_color=[0, 0, 0, 1],
        )

        input_box.add_widget(self.txt_input)
        self.window.add_widget(input_box)

        self.scan_button = Button(
            text="TAKE AN IMAGE",
            size_hint=(0.9, 0.15),
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            bold=True,
            background_color=(0.2, 0.8, 1, 1),
            color=(1, 1, 1, 1),
            font_size=18
        )
        self.scan_button.bind(on_press=self.save_image)
        self.window.add_widget(self.scan_button)

        self.gallery_button = Button(
            text="VIEW GALLERY",
            size_hint=(1, 0.15),
            bold=True,
            background_color=(0.2, 0.7, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size=18
        )
        self.window.add_widget(self.gallery_button)

        if platform == "android":
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

        return self.window

    def update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def timestamp_filename(self):
        current_time = datetime.datetime.now()
        return current_time.strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"

    def get_current_timestamp(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def show_loading_popup(self, message="Processing..."):
        self.loading_popup = Popup(
            title='Please Wait',
            content=Label(text=message, font_size='16sp', color=[1, 1, 1, 1]),
            size_hint=(None, None),
            size=(300, 150),
            auto_dismiss=False,
            background_color=(0.1, 0.1, 0.1, 0.9)
        )
        self.loading_popup.open()

    def hide_loading_popup(self):
        if hasattr(self, 'loading_popup') and self.loading_popup:
            self.loading_popup.dismiss()

    def show_notification(self, message):
        layout = FloatLayout()
        notif_label = Label(
            text=message,
            font_size='16sp',
            size_hint=(None, None),
            size=(300, 150),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            color=(1, 1, 1, 1)
        )
        layout.add_widget(notif_label)

        popup = Popup(
            title='Notification',
            content=layout,
            size_hint=(None, None),
            size=(350, 180),
            background_color=(0.1, 0.1, 0.1, 0.9),
            auto_dismiss=False
        )

        anim = Animation(opacity=0, duration=0.5)
        popup.open()

        def dismiss_popup(*args):
            anim.start(popup)
            Clock.schedule_once(lambda dt: popup.dismiss(), 0.5)

        Clock.schedule_once(dismiss_popup, 2.5)

    def save_image(self, instance):
        """ Call the server to retrieve the image capture on ESP32 CAM and Save the image to the phone's local storage """
        image_url="http://"+self.txt_input.text
        print("Url pointing to the esp32: ", image_url)
        print("type: ", type(image_url))
        if platform == "android":
            try:
                pythonActivity=autoclass("org.kivy.android.PythonActivity")
                app_context=pythonActivity.mActivity.getApplicationContext()
                private_dir=app_context.getFilesDir().getAbsolutePath()
                os.makedirs(private_dir, exist_ok=True)
                save_path=os.path.join(private_dir, "downloaded_image.jpg")
                response=requests.get(image_url, stream=True)
                if response.status_code==200:
                    with open(save_path, "wb") as file:
                        for chunk in response.iter_content(1024):
                            file.write(chunk)
                    ss=SharedStorage()
                    ss.copy_to_shared(save_path, filepath="/storage/emulated/0/SenseMate/records/"+self.timestamp_filename())
                else:
                    print("Failed to download the image with a response status code : ", response.status_code)
            except Exception as e:
                print(f"Error saving image: {e}")
        image_url = self.txt_input.text.strip()
        if not image_url:
            self.show_notification("Enter a valid ESP IP address!")
            return

        self.show_notification("Capturing image...\n" + self.get_current_timestamp())
        self.show_loading_popup("Capturing image from ESP...")

if __name__ == "__main__":
    SenseMate().run()
