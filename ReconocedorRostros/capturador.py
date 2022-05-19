import cv2
import os
import imutils

class Capturador:
	def __init__(self, identificador):
		self.identificador = identificador
		self.dataPath = "./Data"
		self.completePath = self.dataPath + "/" + identificador
 
	def crearCarpeta(self):
		if not os.path.exists(self.completePath):
			os.makedirs(self.completePath)
			return True
		

	def capturar(self):
		cap = cv2.VideoCapture(2)
		
		faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
		count = 0

		while True:

			ret, frame = cap.read()
			if ret == False: break
			frame =  imutils.resize(frame, width=640)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			auxFrame = frame.copy()

			faces = faceClassif.detectMultiScale(gray,1.3,5)

			for (top,right,bottom,left) in faces:
				cv2.rectangle(frame, (top,right),(top+bottom,right+left),(0,255,0),2)
				
				y = top - 15 if top - 15 > 15 else top + 15
				cv2.putText(frame, 'identificando', (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
				#rostro = auxFrame[y:y+h,x:x+w]
				#rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
				#cv2.imwrite(personPath + '/rotro_{}.jpg'.format(count),rostro)
				count = count + 1
			cv2.imshow('frame',frame)

			k =  cv2.waitKey(1)
			if k == 27 or count >= 300:
				break

		cap.release()
		cv2.destroyAllWindows()

c = Capturador('edgar')
c.capturar()