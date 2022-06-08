import cv2


def detect_face(img):
    #Convierta la imagen en una imagen en escala de grises, porque el detector facial OpenCV necesita una imagen en escala de grises

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Cargue el reconocedor de rostros OpenCV, tenga en cuenta que la ruta aquí es la ubicación que guardó cuando descargó el reconocedor
    face_cascade = cv2.CascadeClassifier(r'lbpcascade_frontalface.xml')

    #scaleFactor representa la proporción de cada reducción del tamaño de la imagen, minNeighbors representa el número mínimo de rectángulos adyacentes que constituyen el objetivo de detección
    #Aquí seleccione el tamaño de la imagen que se reducirá 1,2 veces. Cuanto más grande sea el minNeighbors, más precisa será la cara reconocida, pero también es fácil pasar por alto
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=1)

    # Si no hay rostro en la imagen, la imagen no participará en el entrenamiento, regrese Ninguno
    if len(faces) == 0:
        return None, None

    # Extraer zona facial
    (x, y, w, h) = faces[0]

    #Volver al rostro y su zona
    return gray[y:y + w, x:x + h], faces[0]

# frame = cv2.imread('./cr7.jpeg')
# face, rect = detect_face(frame)
# cv2.imshow('Imagen convertida a grises',face)
# cv2.waitKey(0)
