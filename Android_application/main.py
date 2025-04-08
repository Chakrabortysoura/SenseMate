import os
import requests
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image as widget_image
from kivy.utils import platform
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
import datetime
from jnius import autoclass
if platform == "android":
    from android.permissions import request_permissions, Permission
    from androidstorage4kivy import SharedStorage
class SenseMate(App):

    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.color = '#0F0F0F'
        # add widgets to window

        # image widget
        self.window.add_widget(widget_image(source="sensemate.png"))

        # label widget
        self.txt = Label(
            text=" All pictures captured are stored in /Downloads/SenseMate/",
            font_size=20,
            color='#EA6191'
        )
        self.window.add_widget(self.txt)

        self.txt_input = TextInput(
            hint_text="Give IP address of the ESP"
        )
        self.window.add_widget(self.txt_input)

        self.scan_button = Button(
            text="TAKE AN IMAGE",
            size_hint=(1, 0.5),
            bold=True,
            background_color='#EA6191'

        )
        self.scan_button.bind(on_press=self.save_image)
        self.window.add_widget(self.scan_button)
        # Request permissions on Android
        if platform == "android":
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

        return self.window

    def timestamp_filename(self):
        """"Create timestamped name for the current image to be saved"""
        current_time=str(datetime.datetime.now())
        return current_time[:current_time.rindex('.')].replace(' ','_')+".jpg"

    def scan_file(self, file_path):
        """ Notify the media scanner to make the file visible in the gallery """
        MediaScannerConnection = autoclass('android.media.MediaScannerConnection')
        Uri = autoclass('android.net.Uri')
        context = autoclass('org.kivy.android.PythonActivity').mActivity.getApplicationContext()
        MediaScannerConnection.scanFile(context, [file_path], None, None)

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

if __name__ == "__main__":
    SenseMate().run()