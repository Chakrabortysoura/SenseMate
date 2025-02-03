from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from jnius import autoclass
from android.permissions import request_permissions, Permission
# from android.storage import app_storage_path
import android

# Access MediaStore API
MediaStore = autoclass('android.provider.MediaStore')
ContentValues = autoclass('android.content.ContentValues')
Environment = autoclass('android.os.Environment')
BluetoothAdapter=autoclass("android.bluetooth.BluetoothAdapter")
BluetoothDevice=autoclass("android.bluetooth.BluetoothDevice")
BluetoothSocket=autoclass("android.bluetooth.BluetoothSocket")
UUID=autoclass("java.util.UUID")

TARGET_MAC="EC:64:C9:99:65:AA"
UUID_SPP=UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")

class Sensemate(App):
    save_path = "/received_image.jpg"

    def print_message(self):
        print("The message was=>")
        print(self.txt_input.text)

    def save_image_to_download(self, image_data):
        # Prepare the file to save
        context = android.activity.getApplicationContext()
        values = ContentValues()
        values.put(MediaStore.Images.Media.TITLE, "received_image.jpg")
        values.put(MediaStore.Images.Media.DISPLAY_NAME, "received_image.jpg")
        values.put(MediaStore.Images.Media.MIME_TYPE, "image/jpeg")

        # Get external storage directory (Downloads folder)
        downloads_dir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS)
        file_uri = context.getContentResolver().insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values)

        # Open file and write image data
        output_stream = context.getContentResolver().openOutputStream(file_uri)
        output_stream.write(image_data)
        output_stream.close()


    def send_message(self, instance):
        message=self.txt_input.text
        adapter=BluetoothAdapter.getDefaultAdapter()
        if adapter is None:
            self.txt.text="Bluetooth not supported on this device"
            return

        if not adapter.isEnabled():
            self.txt.text="Please Enable Bluetooth"
            return
        device=adapter.getRemoteDevice(TARGET_MAC)
        socket=device.createRfcommSocketToServiceRecord(UUID_SPP)
        try:
            socket.connect()
            socket.getOutputStream().write(message.encode())
            self.txt.text="Message sent successfully"
            input_stream=socket.getInputStream()

            size_data=bytearray(4)
            bytes_read=input_stream.read(size_data, 0, 4)

            if bytes_read<4:
                self.txt.text="Image size not received properly"
                return

            image_size=int.from_bytes(size_data, byteorder='little')
            self.txt.text=f"Image size: {image_size}"

            image_data = bytearray()
            buffer = bytearray(1024)  # Temporary buffer
            total_received = 0
            while total_received < image_size:
                bytes_to_read = min(1024, image_size - total_received)
                bytes_read = input_stream.read(buffer, 0, bytes_to_read)

                if bytes_read == -1:
                    print("Connection lost!")
                    break

                image_data.extend(buffer[:bytes_read])
                total_received += bytes_to_read

            self.save_image_to_download(image_data)
            self.txt.text="Image received successfully"
            socket.close()

        except Exception as e:
            self.txt.text=f"Error : {str(e)}"


    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6,0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.color = '#0F0F0F'
        #add widgets to window

        #image widget
        self.window.add_widget(Image(source="sensemate.png"))

        #label widget
        self.txt = Label(
            text=self.save_path,
            font_size = 20,
            color = '#EA6191'
            )
        self.window.add_widget(self.txt)

        self.txt_input=TextInput(
            hint_text="Enter the message to send..."
        )
        self.window.add_widget(self.txt_input)

        self.scan_button = Button(
            text="Send Message",
            size_hint = (1, 0.5),
            bold = True,
            background_color = '#EA6191'
            )
        self.scan_button.bind(on_press=self.send_message)
        self.window.add_widget(self.scan_button)

        request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
        return self.window

if __name__ == "__main__":
    Sensemate().run()
