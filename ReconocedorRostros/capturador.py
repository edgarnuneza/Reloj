import cv2
import os
import imutils
import shutil

class Capturador:
	def __init__(self, identificador=""):
		self.identificador = identificador
		self.dataPath = "./Data/FotosEntrenamiento"
		self.completePath = self.dataPath + "/" + identificador
		self.count = 0
		self.limite = 300
		self.detener = False
 
	def crearCarpeta(self):
		if self.identificador == '':
			return False

		if os.path.exists(self.completePath):
			shutil.rmtree(self.completePath)

		if not os.path.exists(self.completePath):
			os.makedirs(self.completePath)
			return True
		
	def capturar(self):
		self.completePath = self.dataPath + "/" + self.identificador
		self.crearCarpeta()

		if self.identificador == '':
			return False

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

			(flag, encodedImage) = cv2.imencode(".jpg", frame)
			if not flag:
				continue
			yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                bytearray(encodedImage) + b'\r\n')

			if self.count >= self.limite:
				self.detener = True
				break

			# cv2.imshow('frame',frame)

			# k =  cv2.waitKey(1)
			# if k == 27 or self.count >= self.limite:
			# 	break

		self.detener = True
		cap.release()
		#cv2.destroyAllWindows()

		if self.count < self.limite:
			shutil.rmtree(self.completePath)
			return False


		self.count = 0
		return True

# c = Capturador('edgar')
# print(c.capturar())