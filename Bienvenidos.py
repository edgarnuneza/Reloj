from pathlib import Path

import tkinter as tk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def createWindow(app):
    window = tk.Toplevel(app)
    # Medidas y color de la ventana
    alto = 700
    ancho = 980

    x_ventana = window.winfo_screenwidth() // 2 - ancho // 2
    y_ventana = window.winfo_screenheight() // 2 - alto // 2
    posicion = str(ancho) + "x" + str(alto) + \
        "+" + str(x_ventana) + "+" + str(y_ventana)
    window.geometry(posicion)
    window.configure(bg="#FFFFFF")

    window.configure(bg = "#FFFFFF")


    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = alto,
        width = ancho,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        700,
        1000.0,
        540.0,
        fill="#e73636",
        outline="")

    canvas.create_rectangle(
        90.0,
        80.0,
        500.0,
        alto-50,
        fill="#000000",
        outline="")


    canvas.create_text(
        600,
        150.0,
        anchor="nw",
        text="BIENVENIDO",
        fill="#000000",
        font=("Inter", 32 * -1)
    )

    canvas.create_text(
        600.0,
        240.0,
        anchor="nw",
        text="Nombre: ",
        fill="#000000",
        font=("Inter", 28 * -1)
    )

    canvas.create_text(
        600.0,
        300.0,
        anchor="nw",
        text="Matricua: ",
        fill="#000000",
        font=("Inter", 28 * -1)
    )

    canvas.create_text(
        600.0,
        360.0,
        anchor="nw",
        text="Fecha: ",
        fill="#000000",
        font=("Inter", 28 * -1)
    )

    canvas.create_text(
        600.0,
        420.0,
        anchor="nw",
        text="Hora: ",
        fill="#000000",
        font=("Inter", 28 * -1)
    )


    window.resizable(False, False)
    window.mainloop()

    #listo xd