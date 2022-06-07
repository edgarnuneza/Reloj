import os

#Introduzca el archivo fuente recién escrito
from detect_face import detect_face
import cv2


def prepare_training_data():
    # Lee el nombre de la imagen en la carpeta de entrenamiento
    dirs = os.listdir(r'./img_train')
    faces = []
    labels = []
    for image_path in dirs:
        #Si el nombre de la imagen comienza con feliz, la etiqueta es 1l; triste comienza con la etiqueta 2
        if image_path[0] == 'h':
            label = 1
        if image_path[0] == 's':
            label = 2
        if image_path[0] == 'a':
            label = 3
        if image_path[1] == 'u':
            label = 4

        #Obtener ruta de imagen
        image_path = './img_train/' + image_path

        #Volver a escala de grises, volver al objeto Mat
        image = cv2.imread(image_path,0)

        # Mostrar imagen en forma de ventana, mostrar 100 milisegundos
        # cv2.imshow("Training on image...", image)
        # cv2.waitKey(100)

        # Llame a la función que escribimos anteriormente
        face, rect = detect_face(image)
        if face is not None:
            faces.append(face)
            labels.append(label)

    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()

    return faces, labels

