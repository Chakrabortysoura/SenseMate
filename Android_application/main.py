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
    from jnius import autoclass, cast


class SenseMate(App):

    def build(self):
        self.window = GridLayout(cols=1, size_hint=(0.8, 0.9), pos_hint={"center_x": 0.5, "center_y": 0.5})

        # Robotic Theme Background
        self.window.canvas.before.clear()
        with self.window.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.05, 0.07, 0.1, 1)
            self.bg_rect = Rectangle(pos=self.window.pos, size=self.window.size)
            self.window.bind(pos=self.update_bg, size=self.update_bg)

        self.window.add_widget(widget_image(source="sensemate.png"))

        # IP Input
        input_box = BoxLayout(orientation='vertical', size_hint=(0.9, None), height=60, pos_hint={'center_x': 0.5},
                              padding=[10, 10], spacing=5)

        self.txt_input = TextInput(hint_text="Enter IP address of the ESP", size_hint=(1, 1),
                                   font_size='18sp', halign="center",
                                   background_color=[1, 1, 1, 1], foreground_color=[0, 0, 0, 1])
        input_box.add_widget(self.txt_input)
        self.window.add_widget(input_box)

        # Take Image Button
        self.scan_button = Button(text="TAKE AN IMAGE", size_hint=(0.9, 0.15),
                                  pos_hint={'center_x': 0.5}, bold=True,
                                  background_color=(0.2, 0.8, 1, 1), color=(1, 1, 1, 1), font_size=18)
        self.scan_button.bind(on_press=self.save_image)
        self.window.add_widget(self.scan_button)

        # Gallery Button
        self.gallery_button = Button(text="VIEW GALLERY", size_hint=(1, 0.15),
                                     bold=True, background_color=(0.2, 0.7, 0.3, 1),
                                     color=(1, 1, 1, 1), font_size=18)
        self.window.add_widget(self.gallery_button)

        if platform == "android":
            request_permissions([
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.INTERNET,
                Permission.ACCESS_NETWORK_STATE,
                Permission.VIBRATE
            ])

        return self.window

    def update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def timestamp_filename(self):
        current_time = datetime.datetime.now()
        return current_time.strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"

    def get_current_timestamp(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def show_toast(self, title, message):
        # Desktop/Universal toast-style popup
        layout = FloatLayout()
        notif_label = Label(
            text=f"[b]{title}[/b]\n{message}",
            markup=True,
            font_size='16sp',
            size_hint=(None, None),
            size=(300, 150),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            color=(1, 1, 1, 1)
        )
        layout.add_widget(notif_label)

        popup = Popup(
            title='',
            content=layout,
            size_hint=(None, None),
            size=(350, 160),
            background_color=(0, 0, 0, 0.8),
            auto_dismiss=False,
            separator_height=0
        )

        popup.open()
        anim = Animation(opacity=0, duration=0.5)
        Clock.schedule_once(lambda dt: anim.start(popup), 2)
        Clock.schedule_once(lambda dt: popup.dismiss(), 2.5)

    def notify(self, title, message):
        if platform == 'android':
            try:
                from jnius import autoclass, cast
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Context = autoclass('android.content.Context')
                NotificationManager = autoclass('android.app.NotificationManager')
                NotificationChannel = autoclass('android.app.NotificationChannel')
                NotificationBuilder = autoclass('android.app.Notification$Builder')
                Build_VERSION = autoclass('android.os.Build$VERSION')

                activity = PythonActivity.mActivity
                context = cast('android.content.Context', activity.getApplicationContext())

                channel_id = "sensemate_channel"
                channel_name = "SenseMate Alerts"
                importance = NotificationManager.IMPORTANCE_HIGH
                notification_service = cast(NotificationManager, context.getSystemService(Context.NOTIFICATION_SERVICE))

                if Build_VERSION.SDK_INT >= 26:
                    channel = NotificationChannel(channel_id, channel_name, importance)
                    channel.setDescription("Channel for SenseMate alerts")
                    notification_service.createNotificationChannel(channel)
                    builder = NotificationBuilder(context, channel_id)
                else:
                    builder = NotificationBuilder(context)

                builder.setContentTitle(title)
                builder.setContentText(message)
                builder.setSmallIcon(activity.getApplicationInfo().icon)
                builder.setAutoCancel(True)

                notification_service.notify(1, builder.build())
            except Exception as e:
                print(f"[Android Notification Error]: {e}")
        else:
            try:
                from plyer import notification
                notification.notify(
                    title=title,
                    message=message,
                    timeout=5  # duration in seconds
                )
            except Exception as e:
                print(f"[Desktop Notification Error]: {e}")


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

    def save_image(self, instance):
        ip = self.txt_input.text.strip()
        if not ip:
            self.notify("SenseMate", "Enter a valid ESP IP address!")
            return

        self.notify("SenseMate", f"Capturing image at {self.get_current_timestamp()}")
        self.show_loading_popup("Capturing image from ESP...")

        image_url = "http://" + ip
        print("URL pointing to the ESP32:", image_url)

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
                    print("Failed to download image. Status:", response.status_code)
            except Exception as e:
                print(f"Error saving image: {e}")
        else:
            # For desktop simulation, just simulate download
            print(f"[SIMULATION] Image downloaded from: {image_url}")

        Clock.schedule_once(lambda dt: self.hide_loading_popup(), 2)


if __name__ == "__main__":
    SenseMate().run()
