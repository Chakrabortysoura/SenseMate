import os
import requests
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image as widget_image
from kivy.utils import platform
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
import datetime

if platform == "android":
    from android.permissions import request_permissions, Permission
    from androidstorage4kivy import SharedStorage

class SenseMate(App):

    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.8, 0.9)  # More screen coverage, better fit
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # Background color update
        self.window.canvas.before.clear()
        with self.window.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.1, 0.1, 0.3, 1)  # Deep blue background
            self.bg_rect = Rectangle(pos=self.window.pos, size=self.window.size)
            self.window.bind(pos=self.update_bg, size=self.update_bg)

        # Image widget
        self.window.add_widget(widget_image(source="sensemate.png"))

    #     # Label Widget - Adjusts with Aspect Ratio
    #     self.txt = Label(
    # text="All pictures captured are stored in /Downloads/SenseMate/",
    # font_size='18sp',
    # color='#EA6191',
    # halign="center",
    # size_hint=(0.9, None),  # Responsive width, dynamic height
    # text_size=(self.window.width * 0.9, None),  # Auto-wrap text
    # height=50  # Ensures it remains visible
    # )
    #     self.window.add_widget(self.txt)

        # Box for TextInput - Bigger & Raised Higher
        input_box = BoxLayout(
    orientation='vertical',
    size_hint=(0.9, None),  # Bigger width
    height=60,  # Increased height
    pos_hint={'center_x': 0.5, 'center_y': 0.65},  # Shifted upwards
    padding=[10, 10],
    spacing=5
)

        self.txt_input = TextInput(
            hint_text="Enter IP address of the ESP",
            size_hint=(1, 1),  # Uses full box width
            font_size='18sp',
            halign="center",
            background_color=[1, 1, 1, 1],  # White background
            foreground_color=[0, 0, 0, 1],  # Black text
        )

        # Add TextInput inside the Box
        input_box.add_widget(self.txt_input)
        self.window.add_widget(input_box)

        # Capture Image Button - Raised Higher
        self.scan_button = Button(
            text="TAKE AN IMAGE",
            size_hint=(0.9, 0.15),  # Increased width
            pos_hint={'center_x': 0.5, 'center_y': 0.55},  # Raised Upwards
            bold=True,
            background_color=(0, 0.6, 1, 1),  # Vibrant blue button
            color=(1, 1, 1, 1),
            font_size=18
        )
        self.scan_button.bind(on_press=self.save_image)
        self.window.add_widget(self.scan_button)
        
        # Additional Button: View Gallery
        self.gallery_button = Button(
            text="VIEW GALLERY",
            size_hint=(1, 0.15),
            bold=True,
            background_color=(0.2, 0.7, 0.2, 1),  # Green button
            color=(1, 1, 1, 1),
            font_size=18
        )
        self.window.add_widget(self.gallery_button)
        
        # Request permissions on Android
        if platform == "android":
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        
        return self.window

    def update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def timestamp_filename(self):
        """Create timestamped name for the current image to be saved"""
        current_time = str(datetime.datetime.now())
        return current_time[:current_time.rindex('.')].replace(' ', '_') + ".jpg"

    def save_image(self, instance):
        """ Call the server to retrieve the image capture on ESP32 CAM and Save the image to the phone's local storage """
        image_url = self.txt_input.text
        print("Url pointing to the esp32: ", image_url)
        if platform == "android":
            try:
                pythonActivity = autoclass("org.kivy.android.PythonActivity")
                app_context = pythonActivity.mActivity.getApplicationContext()
                private_dir = app_context.getFilesDir().getAbsolutePath()
                os.makedirs(private_dir, exist_ok=True)
                save_path = os.path.join(private_dir, "downloaded_image.jpg")
                response = requests.get(image_url, stream=True)
                if response.status_code == 200:
                    with open(save_path, "wb") as file:
                        for chunk in response.iter_content(1024):
                            file.write(chunk)
                    ss = SharedStorage()
                    ss.copy_to_shared(save_path, filepath="/storage/emulated/0/SenseMate/records/" + self.timestamp_filename())
                else:
                    print("Failed to download the image with status code:", response.status_code)
            except Exception as e:
                print(f"Error saving image: {e}")

if __name__ == "__main__":
    SenseMate().run()