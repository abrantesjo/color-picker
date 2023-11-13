import tkinter as tk
from tkinter import ttk #temas do tkinter
import pyautogui #capturar a cor do pixel na tela
from pynput import mouse #ouvir eventos do mouse
import pyperclip #copiar texto
from colorsys import rgb_to_hsv, rgb_to_hls #converter cores
from collections import namedtuple #criar uma namedtuple


CMYKColor = namedtuple("CMYKColor", ["c", "m", "y", "k"])

rgbC, cmykC, hslC, hsvC = 0,0,0,0
class colorPickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Picker")
        self.root.geometry("900x900")
        
       

        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 16))
        style.configure('TLabel', font=('Helvetica', 20))

        self.pick_color_button = ttk.Button(
            self.root, text="Selecione uma cor", command=self.toggle_color_picker)
        self.pick_color_button.pack(pady=20)

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

        self.color_rgb_label = ttk.Label(
        self.root, text="Valor em RGB: ")
        self.color_rgb_label.pack(pady=20)

        self.copy_rgb_button = ttk.Button(
            self.root, text="Copiar valor em RGB", command=self.copy_rgb_value)
        self.copy_rgb_button.pack()

        self.color_cmyk_label = ttk.Label(
        self.root, text="Valor em CMYK: ")
        self.color_cmyk_label.pack(pady=20)

        self.copy_cmyk_button = ttk.Button(
            self.root, text="Copiar valor em CMYK", command=self.copy_cmyk_value)
        self.copy_cmyk_button.pack()

        self.color_hsl_label = ttk.Label(
        self.root, text="Valor em HSL: ")
        self.color_hsl_label.pack(pady=20)

        self.copy_hsl_button = ttk.Button(
            self.root, text="Copiar valor em HSL", command=self.copy_hsl_value)
        self.copy_hsl_button.pack()

        self.color_hsv_label = ttk.Label(
        self.root, text="Valor em HSV: ")
        self.color_hsv_label.pack(pady=20)

        self.copy_hsv_button = ttk.Button(
            self.root, text="Copiar valor em HSV", command=self.copy_hsv_value)
        self.copy_hsv_button.pack()


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
        global rgbC
        if self.copied_color:
            pyperclip.copy(str(rgbC))
    
    def copy_cmyk_value(self):
        global cmykC 
        cmykC = tuple(round(valor*100, 0) for valor in cmykC)
        cmykC = tuple(int(valor) for valor in cmykC)
        print(cmykC)
        if self.copied_color:
            pyperclip.copy("({}%, {}%, {}%, {}%)".format(cmykC[0], cmykC[1], cmykC[2], cmykC[3]))

    def copy_hsl_value(self):
        global hslC
        if self.copied_color:
            pyperclip.copy("({:.2f}, {:.2f}, {:.2f})".format(hslC[0], hslC[1], hslC[2]))

    def copy_hsv_value(self):
        global hsvC
        if self.copied_color:
            pyperclip.copy("({:.2f}, {:.2f}, {:.2f})".format(hsvC[0], hsvC[1], hsvC[2]))

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
        self.color_hex_label.configure(text="Valor em HEX: " + color_hex)
        rgb_color = self.hex_to_rgb(color_hex)
        self.color_rgb_label.configure(text="Valor em RGB: ({}, {}, {})".format(rgb_color[0], rgb_color[1], rgb_color[2]))

        cmyk_color = self.rgb_to_cmyk(rgb_color)
        hsl_color = self.rgb_to_hsl(rgb_color)
        hsv_color = self.rgb_to_hsv(rgb_color)
        
        global rgbC, hslC, cmykC, hsvC
        rgbC, cmykC, hslC, hsvC = rgb_color, cmyk_color, hsl_color, hsv_color
        
        self.color_cmyk_label.configure(text="Valor em CMYK: ({:.2f}, {:.2f}, {:.2f}, {:.2f})".format(*cmyk_color))
        self.color_hsl_label.configure(text="Valor em HSL: ({:.2f}, {:.2f}, {:.2f})".format(hsl_color[0], hsl_color[1], hsl_color[2]))
        self.color_hsv_label.configure(text="Valor em HSV: ({:.2f}, {:.2f}, {:.2f})".format(hsv_color[0], hsv_color[1], hsv_color[2]))

    def rgb_to_cmyk(self, rgb):
        r, g, b = [x / 255.0 for x in rgb] #normaliza os valores RGB
        k = min(1 - r, 1 - g, 1 - b) #calcula o preto como o mínimo entre 1 - R, etc
        c = (1 - r - k) / (1 - k) if (1 - k) > 0 else 0 #cálculo dos componentes
        m = (1 - g - k) / (1 - k) if (1 - k) > 0 else 0
        y = (1 - b - k) / (1 - k) if (1 - k) > 0 else 0
        return CMYKColor(c, m, y, k)

    def rgb_to_hsl(self, rgb):
        r, g, b = [x / 255.0 for x in rgb] #normaliza os valores RGB
        h, l, s = rgb_to_hls(r, g, b) #função da colorsys
        return (h * 360, s * 100, l * 100) #obter o ângulo em graus

    def rgb_to_hsv(self, rgb):
        r, g, b = [x / 255.0 for x in rgb] #normaliza os valores RGB
        h, s, v = rgb_to_hsv(r, g, b) #função da colorsys
        return (h * 360, s * 100, v * 100) #obter o ângulo em graus

    def clear_color(self):
        self.color_canvas.configure(bg="white")
        self.color_hex_label.configure(text="Valor em HEX: ")

if __name__ == "__main__":
    root = tk.Tk()
    app = colorPickerApp(root)
    root.mainloop()
