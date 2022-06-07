from detect_face import detect_face

# No hemos preparado estos dos archivos
from draw_text import draw_text


def predict(test_img, face_recognizer):
    # Convertir etiquetas 1, 2 en texto
    subjects = ['', 'Happy', 'Sad', 'Angry', 'Surprise']

    # Obtenga una copia de la imagen
    img = test_img.copy()

    # Detecta la cara de la imagen
    face, rect = detect_face(img)

    # Utilice nuestro reconocedor de rostros para predecir la imagen
    label = face_recognizer.predict(face)
    # Obtiene el nombre de la etiqueta correspondiente devuelta por el reconocedor de caras
    label_text = subjects[label[0]]

    # ¡Tenga en cuenta que aún no hemos escrito las siguientes dos funciones! ! !
    # Marque las emociones faciales alrededor del rectángulo
    draw_text(img, label_text, rect[0], rect[1] - 5)

    return img

