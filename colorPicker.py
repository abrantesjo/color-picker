import tkinter as tk
from tkinter import ttk
import pyautogui
from pynput import mouse
import pyperclip

class colorPickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Picker")
        self.root.geometry("500x500")

        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 16))
        style.configure('TLabel', font=('Helvetica', 20))

        self.color_label = ttk.Label(
            self.root, text="Cor selecionada: ")
        self.color_label.pack(pady=20)

        self.color_canvas = tk.Canvas(
            self.root, width=100, height=100,
            highlightthickness=2, highlightbackground="black")
        self.color_canvas.pack()

        self.color_hex_label = ttk.Label(
            self.root, text="Valor em HEX: ")
        self.color_hex_label.pack(pady=20)

        self.copy_hex_button = ttk.Button(
            self.root, text="Copiar valor em HEX", command=self.copy_hex_value)
        self.copy_hex_button.pack()

        self.pick_color_button = ttk.Button(
            self.root, text="Selecione uma cor", command=self.toggle_color_picker)
        self.pick_color_button.pack(pady=20)

        self.color_rgb_label = ttk.Label(
        self.root, text="Valor em RGB: (0, 0, 0)")
        self.color_rgb_label.pack(pady=20)

        self.copy_rgb_button = ttk.Button(
        self.root, text="Copiar valor em RGB", command=self.copy_rgb_value)
        self.copy_rgb_button.pack()


        self.picking_color = False
        self.listener = None
        self.clear_color()
        self.copied_color = None
        self.copied_rgb_color = None

    def toggle_color_picker(self):
        if self.picking_color:
            self.picking_color = False
            self.picking_color_button.configure(text="Selecione uma cor")
            self.stop_listener()
        else:
            self.picking_color = True
            self.pick_color_button.configure(text="Selecionando uma cor, clique em algum lugar")
            self.start_listener()

    def copy_hex_value(self):
        if self.copied_color:
            pyperclip.copy(self.copied_color)

    def copy_rgb_value(self):
        if self.copied_rgb_color:
            pyperclip.copy(self.copied_rgb_color)


    def start_listener(self):
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()

    def stop_listener(self):
        if self.listener:
            self.listener.stop()
            self.listener = None

    def on_click(self, x, y, button, pressed):
        if pressed:
            color = pyautogui.screenshot(region=(x, y, 1, 1)).getpixel((0, 0))
            color_hex = self.rgb_to_hex(color)
            self.copied_color = color_hex
            rgb_color = self.hex_to_rgb(color_hex)
            self.copied_rgb_color = "RGB: ({}, {}, {})".format(rgb_color[0], rgb_color[1], rgb_color[2])
            self.update_color(color_hex)
            self.picking_color = False
            self.pick_color_button.configure(text="Selecione uma cor")
            self.stop_listener()


    def rgb_to_hex(self, rgb):
        return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

    def hex_to_rgb(self, hex_color):
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return (r, g, b)
        
    def update_color(self, color_hex):
        self.color_canvas.configure(bg=color_hex)
        self.color_hex_label.configure(text="Valor em HEX" + color_hex)
        rgb_color = self.hex_to_rgb(color_hex)
        self.color_rgb_label.configure(text="Valor em RGB: ({}, {}, {})".format(rgb_color[0], rgb_color[1], rgb_color[2]))

    def clear_color(self):
        self.color_canvas.configure(bg="white")
        self.color_hex_label.configure(text="Valor em HEX: ")

if __name__ == "__main__":
    root = tk.Tk()
    app = colorPickerApp(root)
    root.mainloop()
