import threading
import time
import os
import requests
import datetime
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image as widget_image
from kivy.utils import platform
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
import cv2
import numpy as np
import kivy.utils

if platform == "android":
    from model import TensorFlowModel
    from android.permissions import request_permissions, Permission
    from androidstorage4kivy import SharedStorage
    from jnius import autoclass, cast


class SenseMate(App):
    control_value=False
    def build(self):
        if platform == 'android':
            self.litemodel=TensorFlowModel()
            self.litemodel.load(os.getcwd()+"/model1.tflite")

        self.window = GridLayout(cols=1, size_hint=(1, 1), pos_hint={"center_x": 0.5, "center_y": 0.5}, padding=[20,60,20,200],height=200,spacing=100) # spacing determines the space between the objects

        # Robotic Theme Background
        self.window.canvas.before.clear()
        with self.window.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(8/255, 16/255, 22/255, 1)
            self.bg_rect = Rectangle(pos=self.window.pos, size=self.window.size)
            self.window.bind(pos=self.update_bg, size=self.update_bg)

        self.window.add_widget(widget_image(source="sensemate.png",size_hint=(2,2)))

        # IP Input
        input_box = BoxLayout(orientation='vertical', size_hint=(0.5, None), height=180, pos_hint={'center_x': 0.5 },
                              padding=[50, 20], spacing=20)
        self.txt_input = TextInput(hint_text="Enter IP address of the ESP", size_hint=(1, 1),
                                   font_size='35sp', 
                                   halign="center",
                                   background_color=[1, 1, 1, 1], 
                                   foreground_color=[0, 0, 0, 1])
        input_box.add_widget(self.txt_input)
        self.window.add_widget(input_box)

        # Take Image Button
        scan_button_box = BoxLayout(size_hint=(1, None), height=90, padding=[0, 10])
        self.scan_button = Button(text="START IMAGE CAPTURE", 
                                  size_hint=(0.8, None),
                                  height=120,
                                  pos_hint={'center_x': 0.5},
                                  bold=True, 
                                  background_normal='',
                                  background_color=(kivy.utils.get_color_from_hex("#42FF3EFF")), 
                                  color=(kivy.utils.get_color_from_hex("#391F34FF")), 
                                  font_size=45)


        self.scan_button.bind(on_press=self.save_image)
        scan_button_box.add_widget(self.scan_button)
        self.window.add_widget(scan_button_box)

        gallery_button_box = BoxLayout(size_hint=(1, None), height=90, padding=[0, 10])
        self.gallery_button = Button(text="VIEW GALLERY", 
                                     size_hint=(0.8, None),
                                     height=120,
                                     bold=True, 
                                     background_normal='', 
                                     background_color=(kivy.utils.get_color_from_hex("#FFF826FF")),
                                     color=(kivy.utils.get_color_from_hex("#0B2C39FF")), 
                                     font_size=45)


        gallery_button_box.add_widget(self.gallery_button)
        self.window.add_widget(gallery_button_box)

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
        current_time = str(datetime.datetime.now())
        return current_time[:current_time.rindex('.')].replace(' ', '_') + ".jpg"

    def notify(self, title, message):
        if platform == 'android':
            try:
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

    def save_image_routine(self):
        while self.control_value:
            ip = self.txt_input.text.strip()
            if not ip:
                self.notify("SenseMate", "Enter a valid ESP IP address!")
                return
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
                        # image=np.frombuffer(response.content, np.uint8)
                        # image=cv2.imdecode(image, cv2.IMREAD_COLOR)
                        # image = cv2.resize(image, (150, 150))
                        # image=image.astype(np.float32)/255.0
                        # result= self.litemodel.pred(image)
                        # if np.round(result[[0]]) ==0 :
                        #    self.notify("SenseMate", "Person Detected")
                        with open(save_path, "wb") as file:
                            for chunk in response.iter_content(1024):
                                file.write(chunk)
                        ss = SharedStorage()
                        ss.copy_to_shared(save_path,filepath="/storage/emulated/0/SenseMate/records/" + self.timestamp_filename())
                        self.notify("SenseMate", "Image Captured")
                    else:
                        self.notify("SenseMate", "Device is not found on the address")
                except Exception as e:
                    self.notify("SenseMate", "Some unexpected error encoutered")
            time.sleep(4)
        return

    def save_image(self, instance):
        if not self.control_value:
            self.control_value=True
            threading.Thread(target=self.save_image_routine).start()
            self.scan_button.text="STOP CAPTURE"
        else:
            self.control_value=False
            self.scan_button.text="START CAPTURE"

if __name__ == "__main__":
    SenseMate().run()