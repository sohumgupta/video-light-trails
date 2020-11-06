import numpy as np
import cv2
from threading import Thread

class VideoGet:
	"""
	Class that continuously gets frames from a VideoCapture object
	with a dedicated thread.
	"""

	def __init__(self, src=0, save_video=False):
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()
		self.stopped = False
		if save_video:
			frame_width = int(self.stream.get(3)) 
			frame_height = int(self.stream.get(4)) 
			self.size = (frame_width, frame_height) 
			self.result = cv2.VideoWriter('out.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, self.size) 

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

def multithread(src, save_video=True):
	save_video = True
	video_getter = VideoGet(src, save_video).start()

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
		# out = (np.max(echoes_np, axis=0))
		# out = np.mean(echoes_np, axis=0).astype(np.uint8)
		out = ((np.max(echoes_np, axis=0) * 0.6 + np.mean(echoes_np, axis=0) * 0.4)).astype(np.uint8)

		# Display the resulting frame
		cv2.imshow('frame', out)
		if save_video:
			video_getter.result.write(out)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			video_getter.stop()
			break

def singlethread(src, save_video=True, downscale=4):
	stream = cv2.VideoCapture(src)

	frame_width = int(stream.get(3)) 
	frame_height = int(stream.get(4)) 
	
	out_width = frame_width // downscale
	out_height = frame_height // downscale

	size = (out_width, out_width) 
	result = cv2.VideoWriter('out.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size) 

	echoes = []
	num_echoes = 60

	while(True):
		grabbed, frame = stream.read()

		if not grabbed:
			break

		# Capture frame-by-frame
		frame = np.array(cv2.resize(frame, size))

		echoes.append(frame)
		if len(echoes) >= num_echoes:
			echoes = echoes[1:]

		# Our operations on the frame come here
		echoes_np = np.array(echoes)
		# out = (np.max(echoes_np, axis=0))
		# out = np.mean(echoes_np, axis=0).astype(np.uint8)
		out = ((np.max(echoes_np, axis=0) * 0.6 + np.mean(echoes_np, axis=0) * 0.4)).astype(np.uint8)

		# Display the resulting frame
		cv2.imshow('frame', out)
		if save_video:
			result.write(out)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# When everything done, release the capture
	cv2.destroyAllWindows()

def residual(src, save_video=True, downscale=4, decay=0.99):
	stream = cv2.VideoCapture(src)

	frame_width = int(stream.get(3)) 
	frame_height = int(stream.get(4)) 
	
	out_width = frame_width // downscale
	out_height = frame_height // downscale

	size = (out_width, out_width) 
	result = cv2.VideoWriter('out.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size) 

	current = None
	num_echoes = 16

	while(True):
		grabbed, frame = stream.read()

		if not grabbed:
			break

		# Capture frame-by-frame
		frame = np.array(cv2.resize(frame, size))

		if current is None:
			current = frame
		else:
			current = current * decay

		# Our operations on the frame come here
		echoes_np = np.array([current.astype(np.uint8), frame])
		current = np.max(echoes_np, axis=0)

		# Display the resulting frame
		cv2.imshow('frame', current)
		if save_video:
			result.write(current)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# When everything done, release the capture
	cv2.destroyAllWindows()

if __name__ == "__main__":
	src = 'P1020780.MP4'
	singlethread(src)
	# residual(src)