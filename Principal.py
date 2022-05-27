
from pathlib import Path

from tkinter import *
# Explicit imports to satisfy Flake8

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from Deteccion import construirVentana

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def iniciar_Sesion():
    construirVentana(window)

window = Tk()

window.geometry("898x507")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 507,
    width = 898,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=582.0,
    y=296.0,
    width=180.0,
    height=59.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=iniciar_Sesion,
    relief="flat"
)
button_2.place(
    x=582.0,
    y=410.0,
    width=180.0,
    height=59.0
)

canvas.create_text(
    559.0,
    193.0,
    anchor="nw",
    text="BIENVENIDO",
    fill="#F20A0A",
    font=("Abel Regular", 48 * -1)
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    683.0,
    90.0,
    image=image_image_1
)

canvas.create_rectangle(
    0.0,
    0.0,
    476.0,
    507.0,
    fill="#E73636",
    outline="")

canvas.create_text(
    25.0,
    59.0,
    anchor="nw",
    text="RELOJ CHECADOR",
    fill="#FFFFFF",
    font=("Abel Regular", 48 * -1)
)

canvas.create_text(
    32.0,
    168.0,
    anchor="nw",
    text="Programa realizado para \nel registro de asistencia\na traves de reconocimiento\nfacial",
    fill="#FFFFFF",
    font=("Abel Regular", 32 * -1)
)
window.resizable(False, False)
window.mainloop()
