from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
#import bluetooth

class Sensemate(App):
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
            text="Mac Address",
            font_size = 20,
            color = '#EA6191'
            )
        self.window.add_widget(self.txt)

        self.scan_button = Button(
            text="Scan for Bluetooth Devices",
            size_hint = (1, 0.5),
            bold = True,
            background_color = '#EA6191'
            )
        self.scan_button.bind(on_press=self.scan_devices)
        self.window.add_widget(self.scan_button)

        self.result_label = Label(
            text="Device MAC Address",
            font_size = 20
            )
        self.window.add_widget(self.result_label)

        return self.window
    
    #fetch mac address
    def scan_devices(self, instance):
        
        #remove return statement when using the function
        return 0
        try:
            # Discover nearby Bluetooth devices
            devices = bluetooth.discover_devices(lookup_names=True)
            if devices:
                device_info = "\n".join(f"{name}: {address}" for address, name in devices)
                self.result_label.text = f"Found Devices:\n{device_info}"
            else:
                self.result_label.text = "No devices found."
        except Exception as e:
            self.result_label.text = f"Error: {str(e)}"


if __name__ == "__main__":
    Sensemate().run()