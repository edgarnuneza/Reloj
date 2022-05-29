import cv2
import os
import imutils
import shutil

class Capturador:
	def __init__(self, identificador):
		self.identificador = identificador
		self.dataPath = "./Data/Fotos/Entrenamiento"
		self.completePath = self.dataPath + "/" + identificador
		self.crearCarpeta()
		self.count = 0
		self.limite = 300
 
	def crearCarpeta(self):
		if not os.path.exists(self.completePath):
			os.makedirs(self.completePath)
			return True
		
	def capturar(self):
		cap = cv2.VideoCapture(0)
		
		faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
		self.count = 0

		while True:

			ret, frame = cap.read()
			if ret == False: break
			frame =  imutils.resize(frame, width=640)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			auxFrame = frame.copy()

			faces = faceClassif.detectMultiScale(gray,1.3,5)

			for (x,y,w,h) in faces:
				cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
				rostro = auxFrame[y:y+h,x:x+w]
				rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
				cv2.imwrite(self.completePath + '/rotro_{}.jpg'.format(self.count),rostro)
				self.count = self.count + 1

			cv2.imshow('frame',frame)

			k =  cv2.waitKey(1)
			if k == 27 or self.count >= self.limite:
				break

		cap.release()
		cv2.destroyAllWindows()

		if self.count < self.limite:
			shutil.rmtree(self.completePath)
			return False

		return True

c = Capturador('edgar')
print(c.capturar())