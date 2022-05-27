from tkinter import *
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
from main import grabar
from tkinter import Tk
from gui import crearVentana
import cv2

def iniciar():
    global cap

    visualizar()

def visualizar():
    global cap
    global lblVideo
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, visualizar)
        else:
            lblVideo.image = ""
            cap.release()

def finalizar():
    global cap
    cap.release()

cap = None


def construirVentana(root):
    '''btnFinalizar = Button(root, text="Finalizar", width=45, command=finalizar)
    btnFinalizar.grid(column=1, row=0, padx=5, pady=5)
    lblVideo = Label(root)
    lblVideo.grid(column=0, row=1, columnspan=2)
    cap = cv2.VideoCapture(0)'''
    # print(grabar())
    # x = grabar()
    # print(x[0])

    window = Tk()
    im = Image.open("./Data/cr.jpg")
    ph = ImageTk.PhotoImage(im)

    label = Label(window, image=ph)
    label.image=ph

    #file=relative_to_assets("cr.jpg")
    crearVentana(window, "./Data/cr.jpg", "edgar")
    
    root.mainloop()


# img = cv2.imread('./images/62ea2016-d892-11ec-b623-7f3fa32a71e8.jpg', 0) 
# cv2.imshow('image',img)
# cv2.waitKey(0)