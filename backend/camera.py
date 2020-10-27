from threading import Thread
import cv2

def decode_fourcc(v):
  v = int(v)
  return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])

class Camera:
	def __init__(self, width, height, brightness, contrast, saturation, hue, gain, exposure, gamma, backlight, temperature, sharpness, src = 0):
		print(brightness, contrast, saturation, hue, gain, exposure, gamma, backlight, temperature, sharpness)
		self.stream = cv2.VideoCapture(src)
		self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
		self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
		self.stream.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
		self.stream.set(cv2.CAP_PROP_CONTRAST, contrast)
		self.stream.set(cv2.CAP_PROP_SATURATION, saturation)
		self.stream.set(cv2.CAP_PROP_HUE, hue)
		self.stream.set(cv2.CAP_PROP_GAIN, gain)
		self.stream.set(cv2.CAP_PROP_EXPOSURE, exposure)
		self.stream.set(cv2.CAP_PROP_GAMMA, gamma)
		self.stream.set(cv2.CAP_PROP_BACKLIGHT, backlight)
		self.stream.set(cv2.CAP_PROP_TEMPERATURE, temperature)
		self.stream.set(cv2.CAP_PROP_SHARPNESS, sharpness)
		self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
		self.grabbed, self.frame = self.stream.read()
		self.stopped = False

	def get(self, t):
		return self.stream.get(t)

	def start(self):
		Thread(target=self.update, args=()).start()
		return self

	def update(self):
		while True:
			if self.stopped:
				return
			(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		return self.frame

	def stop(self):
		self.stopped = True
