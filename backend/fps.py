import datetime
class FPS:
	def __init__(self, limit):
		self.startTime = None
		self.endTime = None
		self.numFrames = 0
		self.limit = limit

	def start(self):
		self.startTime = datetime.datetime.now()
		return self

	def ready(self):
		return (datetime.datetime.now() - self.startTime) / datetime.timedelta(milliseconds = 1) >= (1000 / self.limit) * self.numFrames

	def stop(self):
		self.endTime = datetime.datetime.now()

	def update(self):
		self.numFrames += 1

	def elapsed(self):
		return (self.endTime - self.startTime).total_seconds()

	def fps(self):
		return self.numFrames / self.elapsed()
