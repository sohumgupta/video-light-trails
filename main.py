import numpy as np
import cv2
from threading import Thread

class VideoGet:
	"""
	Class that continuously gets frames from a VideoCapture object
	with a dedicated thread.
	"""

	def __init__(self, src=0):
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()
		self.stopped = False

	def start(self):
		Thread(target=self.get, args=()).start()
		return self

	def get(self):
		while not self.stopped:
			if not self.grabbed:
				self.stop()
			else:
				(self.grabbed, self.frame) = self.stream.read()

	def stop(self):
		self.stopped = True

if __name__ == "__main__":
	video_getter = VideoGet(0).start()

	echoes = []
	num_echoes = 8

	while(True):
		# Capture frame-by-frame
		frame = video_getter.frame
		frame = np.array(frame)

		echoes.append(frame)
		if len(echoes) >= num_echoes:
			echoes = echoes[1:]

		# Our operations on the frame come here
		echoes_np = np.array(echoes)
		out = (np.max(echoes_np, axis=0))
		# out = np.mean(echoes_np, axis=0)).astype(np.uint8)
		# out = ((np.max(echoes_np, axis=0) * 0.8 + np.mean(echoes_np, axis=0) * 0.2)).astype(np.uint8)

		# Display the resulting frame
		cv2.imshow('frame', out)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			video_getter.stop()
			break

	# When everything done, release the capture
	cv2.destroyAllWindows()