import cv2
import threading
import numpy as np
import time
import pyaudio
import wave
import os
import camera
import counter

class AudioRecorder:
	def __init__(self):
		self.FORMAT = pyaudio.paInt16
		self.CHANNELS = 1
		self.SAMPLING_RATE = 44100
		self.CHUNK = 1024
		self.audio = pyaudio.PyAudio()
		self.stream = self.audio.open(
				format = self.FORMAT,
				channels = self.CHANNELS,
				rate = self.SAMPLING_RATE,
				input = True,
				frames_per_buffer = self.CHUNK)

		self.buffer = b''
		self._running = True
	
	def terminate(self):
		self._running = False

	def run(self, path):
		while True:
			data = self.stream.read(self.CHUNK)
			self.buffer += data

			if not self._running:
				wf = wave.open(path, 'wb')
				wf.setnchannels(self.CHANNELS)
				wf.setsampwidth(2)
				wf.setframerate(self.SAMPLING_RATE)
				wf.writeframes(self.buffer)
				wf.close()
				break
		self.stream.stop_stream()
		self.stream.close()
		self.audio.terminate()

class VideoRecorder:
	def __init__(self, brightness, contrast, saturation, hue, gain, exposure, gamma, backlight, temperature, sharpness):
		self._running = True
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
	
	def terminate(self):
		self._running = False

	def run(self, path):
		cap = camera.Camera(self.brightness, self.contrast, self.saturation, self.hue, self.gain, self.exposure, self.gamma, self.backlight, self.temperature, self.sharpness).start()
		fps = cap.get(cv2.CAP_PROP_FPS)
		width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
		height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		out = cv2.VideoWriter(path, fourcc, fps, (width, height))
		print(fps, width, height)
		fp = counter.FPS(fps).start()
		while self._running:
			frame = cap.read()
			if fp.ready():
				out.write(frame)
				fp.update()
		fp.stop()
		print("[INFO] video saved in", path)
		print("[INFO] elasped time: {:.2f}".format(fp.elapsed()))
		print("[INFO] approx. FPS: {:.2f}".format(fp.fps()))
		cap.stop()
		out.release()

if __name__ == '__main__':
	vr = VideoRecorder()
	vrt = threading.Thread(target = vr.run, args=('output.avi',))
	vrt.start()

	'''
	ar = AudioRecorder()
	art = threading.Thread(target = ar.run, args=('output.wav',))
	art.start()
	'''

	time.sleep(2)

	vr.terminate()
#ar.terminate()

	vrt.join()
#art.join()
