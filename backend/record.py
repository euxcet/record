import cv2
import threading
import numpy as np
import time
import os
import camera
import counter


class VideoRecorder:
	def __init__(self, width, height, brightness, contrast, saturation, hue, gain, exposure, gamma, backlight, temperature, sharpness):
		self._running = True
		self.width = width
		self.height = height
		self.brightness = brightness
		self.contrast = contrast
		self.saturation = saturation
		self.hue = hue
		self.gain = gain
		self.exposure = exposure
		self.gamma = gamma
		self.backlight = backlight
		self.temperature = temperature
		self.sharpness = sharpness

		self.cap = camera.Camera(self.width, self.height, self.brightness, self.contrast, self.saturation, self.hue, self.gain, self.exposure, self.gamma, self.backlight, self.temperature, self.sharpness).start()
		self.fps = self.cap.get(cv2.CAP_PROP_FPS)
		self.real_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
		self.real_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
		self.fourcc = cv2.VideoWriter_fourcc(*"MJPG")
	
	def terminate(self):
		self._running = False

	def run(self, path):
		out = cv2.VideoWriter(path, self.fourcc, self.fps, (self.real_width, self.real_height))
		fp = counter.FPS(self.fps).start()
		while self._running:
			frame = self.cap.read()
			if fp.ready():
				out.write(frame)
				fp.update()
		fp.stop()
		print("[INFO] video saved in", path)
		print("[INFO] width:", self.real_width, 'height:', self.real_height)
		print("[INFO] elasped time: {:.2f}".format(fp.elapsed()))
		print("[INFO] approx. FPS: {:.2f}".format(fp.fps()))
		self.cap.stop()
		out.release()

if __name__ == '__main__':
	vr = VideoRecorder(640, 480, 29, 40, 30, -23, 55, 25, 121, 1, 4690, 2)
	vrt = threading.Thread(target = vr.run, args=('output.avi',))
	vrt.start()


	time.sleep(10)

	vr.terminate()

	vrt.join()