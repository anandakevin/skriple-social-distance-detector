# import the necessary packages
from threading import Thread
import sys
import cv2
import time

# import the Queue class from Python 3
if sys.version_info >= (3, 0):
	from queue import Queue

# otherwise, import the Queue class for Python 2.7
else:
	from Queue import Queue

class FileVideoStream:
	def __init__(self, path, width=None, height=None, transform=None, queue_size=128):
		# initialize the file video stream along with the boolean
		# used to indicate if the thread should be stopped or not
		self.stream = cv2.VideoCapture(path)
		# if width != None and height != None:
		# 	print('set width:', width)
		# 	print('set height:', height)
		# 	# self.stream.set(3, width)
		# 	newSize = (width, height)
		# 	self.stream = cv2.resize(self.stream, newSize)
		# 	print('curr width:', self.stream.get(3))
		# 	print('curr height:', self.stream.get(4))
		# if height != None:
			
		# 	self.stream.set(4, height)
			
		


		# # resize image
		

		self.stopped = False
		self.transform = transform

		# initialize the queue used to store frames read from
		# the video file
		self.Q = Queue(maxsize=queue_size)
		# intialize thread
		self.thread = Thread(target=self.update, args=())
		self.thread.daemon = True

	def make_1080p(self):
		self.stream.set(3, 1920)
		self.stream.set(4, 1080)

	def make_720p(self):
		self.stream.set(3, 1280)
		self.stream.set(4, 720)

	def make_480p(self):
		self.stream.set(3, 640)
		self.stream.set(4, 480)

	def change_res(self, width, height):
		self.stream.set(3, width)
		self.stream.set(4, height)

	def start(self):
		# start a thread to read frames from the file video stream
		self.thread.start()
		return self

	def update(self):
		# keep looping infinitely
		while True:
			# if the thread indicator variable is set, stop the
			# thread
			if self.stopped:
				break

			# otherwise, ensure the queue has room in it
			if not self.Q.full():
				# read the next frame from the file
				(grabbed, frame) = self.stream.read()

				# if the `grabbed` boolean is `False`, then we have
				# reached the end of the video file
				if not grabbed:
					self.stopped = True
					
				# if there are transforms to be done, might as well
				# do them on producer thread before handing back to
				# consumer thread. ie. Usually the producer is so far
				# ahead of consumer that we have time to spare.
				#
				# Python is not parallel but the transform operations
				# are usually OpenCV native so release the GIL.
				#
				# Really just trying to avoid spinning up additional
				# native threads and overheads of additional
				# producer/consumer queues since this one was generally
				# idle grabbing frames.
				if self.transform:
					frame = self.transform(frame)

				# add the frame to the queue
				self.Q.put(frame)
			else:
				time.sleep(0.1)  # Rest for 10ms, we have a full queue

		self.stream.release()

	def read(self):
		# return next frame in the queue
		return self.Q.get()

	# Insufficient to have consumer use while(more()) which does
	# not take into account if the producer has reached end of
	# file stream.
	def running(self):
		return self.more() or not self.stopped

	def more(self):
		# return True if there are still frames in the queue. If stream is not stopped, try to wait a moment
		tries = 0
		while self.Q.qsize() == 0 and not self.stopped and tries < 5:
			time.sleep(0.1)
			tries += 1

		return self.Q.qsize() > 0

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
		# wait until stream resources are released (producer thread might be still grabbing frame)
		self.thread.join()