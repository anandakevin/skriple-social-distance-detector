from flask.helpers import make_response
from FileVideoStream import FileVideoStream
from flask import Response, render_template, session, copy_current_request_context
from flask import Flask, url_for, redirect, request
from flask_socketio import SocketIO, emit, disconnect
import threading
import argparse
import time
import cv2
import os
import sys
# import darknet
import json
import time
import socketio

# Add the root directory to sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

from modules import social_distance_detector as sdd

# initialize a flask object
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# app.config['DEBUG'] = True
app_root = os.path.dirname(os.path.abspath(__file__))

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

lock = threading.Lock()

netMain = None
metaMain = None
altNames = None
url = None
vs = None
outputFrame = None
current_page = None
videoPath = None
outputPath = "./Output/video_output.mp4"
template_path = "./templates/"

on_inference = False
video_process = False
model_loaded = False

# pages routing

# main page
@app.route("/")
def index_page():
	global current_page, on_inference
	print('in index')
	if current_page != "index":
		print('before is not index, stopping inference')
		on_inference = False
		print('on inference status:', on_inference)
	current_page = "index"
	print('not in if, on inference status:', on_inference)
	# return the rendered template
	return render_template(template_path + current_page + ".html", sync_mode = socketio.async_mode)

# return page to detect from cam
@app.route("/detect/cam")
def cam_detection_page():
	global current_page, on_inference
	if current_page != "cam_detection":
		on_inference = False
	current_page = "cam_detection"
	if not model_loaded:
		t = threading.Thread(target=init_model)	
		t.daemon = True
		t.start()
	# return render_template(current_page + ".html", sync_mode = socketio.async_mode)
	return render_template(template_path + "realtime.html", sync_mode = socketio.async_mode)

# return page to detect from video
@app.route("/detect/video", methods = ['POST', 'GET'])
def video_detection_page():
	global current_page, on_inference, video_process
	if current_page != "video_detection":
		on_inference = False
	current_page = "video_detection"
	if not model_loaded:
		t = threading.Thread(target=init_model)	
		t.daemon = True
		t.start()
	# return render_template(current_page + ".html", sync_mode = socketio.async_mode)
	return render_template(template_path + "sourcevid.html", sync_mode = socketio.async_mode)

num_of_requests = 0
# starts inference process
# for testing purposes, disable this route, else it will return out of context error
@app.route("/detect/start_inference", methods = ['POST', 'GET'])
def start_inference():
	target = os.path.join(app_root, 'uploaded\\')
	global current_page, num_of_requests
	# from camera
	if request.method == 'GET':
		if current_page == 'cam_detection':
			index = request.values['videoValue']
			print("in GET req, index is:", index)
			setSourceVideo(int(index))
			# setSourceVideo('http://192.168.137.157:8080/video')
	# from file
	elif request.method == 'POST':
		if current_page == 'cam_detection':
			index = int(request.values['videoValue'])
			print("in POST req, index is:", index)
			# setSourceVideo(int(index))
			if index == 0:
				setSourceVideo("./Input/video4_trim.mp4")
			elif index == 3:
				setSourceVideo("./Input/video6.mp4")
		elif current_page == 'video_detection':
			one_file = request.files['video_path']
			file_name = one_file.filename
			dest = ''.join([target, file_name])
			print(dest.replace("\\", "/")) 
			one_file.save(dest)
			setSourceVideo(dest)
	
	# default values, used for testing only
	# if below is used, disable two ifs above
	# from camera
	# if current_page == 'cam_detection':
		# setSourceVideo(0)
	# from file
	# elif current_page == 'video_detection':
	# setSourceVideo("./Input/video3.mp4")
	global on_inference, model_loaded
	num_of_requests += 1
	print("currentReqId :", num_of_requests)
	while True:
		print("waiting for inference to finish and model to be loaded: ", num_of_requests)
		if not on_inference and model_loaded:
			print("inference is finished, starting new thread: ", num_of_requests)
		# start a thread that will perform motion detection
			on_inference = True
			t = threading.Thread(target=detect_people, args=(
				args["frame_count"],))
			t.daemon = True
			t.start()
			
			break

	return str(on_inference)

# stop the inference if currently running
@app.route("/detect/stop_inference", methods = ['POST', 'GET'])
def stop_inference():
	global on_inference
	on_inference = False
	return str(on_inference)

# determine masih jalan apa jalan kaki
@app.route("/detect/get_inference_status", methods = ['GET'])
def inference_status():
	global on_inference
	return str(on_inference)

# @app.route("/detect/set_source_video", methods = ['POST'])
def setSourceVideo(vidPath = 0):
	global videoPath
	videoPath = vidPath

@app.route("/detect/get_source_video", methods = ['GET'])
def getSourceVideo():
	global videoPath
	return videoPath

# return inference result in json
@app.route("/detect/curr_inference_result", methods = ["GET"])
def returnCurrInferRes():
	inferenceRes = sdd.returnInferenceResult()
	json_object = json.dumps(inferenceRes, indent = 4)  
	return json_object

socketio_event_count = 0
def returnInferenceFinishStatus():
	global socketio_event_count
	socketio.emit('finish_inference', namespace='/detect', broadcast=True)
	socketio_event_count += 1
	print('sent event to socket io: ', socketio_event_count)

def returnInferenceResultBySocket():
	inferenceRes = sdd.returnInferenceResult()
	json_object = json.dumps(inferenceRes, indent = 4)  
	print('returnInferenceResultBySocket:', inferenceRes['max_crowd_count'])
	socketio.emit('update_inference', {'data': json_object}, namespace='/detect', broadcast=True)
	socketio_event_count += 1
	print('sent event to socket io: ', socketio_event_count)

def returnInferenceResultAsync():
	global socketio_event_count
	while video_process:
		inferenceRes = sdd.returnInferenceResult()
		json_object = json.dumps(inferenceRes, indent = 4)  
		print('res:', json_object)
		with lock:
			socketio.emit('update_inference', 
							{'data': json_object}, 
							namespace='/detect',
							broadcast=True)
		socketio_event_count += 1
		print('sent event to socket io: ', socketio_event_count)
		socketio.sleep(1)

def returnInferenceResultRefreshPage():

	global current_page
	inferenceRes = sdd.returnInferenceResult()
	json_object = json.dumps(inferenceRes, indent = 4)  
	print('returnInferenceResultRefreshPage:', inferenceRes['max_crowd_count'])
	return render_template(current_page + ".html", sync_mode = socketio.async_mode, infer_res = json_object)

def returnCurrInferResAsResponse2():
	inferenceRes = sdd.returnInferenceResult()
	json_object = json.dumps(inferenceRes, indent = 4)  
	resp = app.response_class(
		response = returnCurrInferRes(),
		mimetype='application/json'
	)
	return resp

def returnCurrInferResAsResponse2():
	def generateInference():
		yield returnCurrInferRes()
	return Response(generateInference(), mimetype="json")

def returnCurrInferResAsResponse3():
	resp = make_response(returnCurrInferRes())

i = 0
# open pipeline to stream video using this url
@app.route("/detect/video_feed")
def video_feed():
	global i
	i += 1
	print('in video feed: ', i)

	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

# helper function to generate frames needed to be streamed
def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock
	# loop over frames from the output stream
	while video_process:
		# wait until the lock is acquired
		# with lock:
		# check if the output frame is available, otherwise skip
		# the iteration of the loop
		if outputFrame is None:
			continue
		# encode the frame in JPEG format
		(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
		# ensure the frame was successfully encoded
		if not flag:
			continue
		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')

# here lies the main function to start predicting people
def detect_people(frameCount):
	"""
	Perform Object detection
	"""
	# grab global references to the video stream, output frame, and
	# lock variables
	global vs, outputFrame, lock, outputPath, num_of_people_at_risk, num_of_groups, crowdCount
	global video_process, on_inference
	sdd_v = sdd.SocialDistanceDetector()
	
	sdd.resetVar()
	cap, frame_width, frame_height, vid_fps = read_video()

	if frame_height > frame_width:
		frame_height = 1280
		frame_width = 720
	else:
		frame_height = 720
		frame_width = 1280	

	frame_height = int(frame_height)
	frame_width = int(frame_width)
	new_height, new_width = frame_height // 2, frame_width // 2
	print("width, height, fps: %s, %s, %s" % (str(frame_width), str(frame_height), str(vid_fps)))	
	# write to output video
	# out = cv2.VideoWriter(outputPath, cv2.VideoWriter_fourcc(*"MPAV"), vid_fps, 
    #                 (frame_width, frame_height))	
	
	# Create an image we reuse for each detect
	darknet_image = darknet.make_image(frame_width, frame_height, 3)
	min_fps = 1000
	max_fps = 0
	fps_count = 0
	total_fps = 0
	total_frame = 0	
	
	video_process = True

	thread_infer_run = False

	while on_inference:
		if model_loaded:
			# if not thread_infer_run: 
			# 	infer_result_thread = threading.Thread(target=returnInferenceResultAsync)	
			# 	infer_result_thread.daemon = True
			# 	infer_result_thread.start()
			# 	thread_infer_run = True

			total_frame += 1
			beg_time = time.time()
			curr_frame = cap.read()
			if curr_frame is None:
				break	
			
			frame_rgb = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2RGB)
			frame_resized = cv2.resize(frame_rgb,
									(frame_width, frame_height),
									interpolation=cv2.INTER_LINEAR)	
			darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())
			detections = darknet.detect_image(netMain, altNames, darknet_image, thresh=0.25)	
			# print(detections)
			image, num_of_people_at_risk, num_of_groups, crowdCount = sdd_v.cvDrawBoxes(detections, frame_resized)
			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

			# count fps
			curr_fps = 1/(time.time()-beg_time)
			processing_time = (time.time()-beg_time) * 100
			min_fps = min(min_fps, curr_fps)
			max_fps = max(max_fps, curr_fps)
			fps_count += 1
			total_fps += curr_fps
			# print("Min FPS:", min_fps)
			# print("Max FPS:", max_fps)
			# print("FPS:", total_fps / total_frame)
			# out.write(image)

			# with lock:
			outputFrame = image.copy()
	
	# release the video stream pointer
	vs.stop()
	video_process = False
	on_inference = False
	print("inference finished")
	time.sleep(2)
	returnInferenceFinishStatus()
	return str("inference finished")

# initialize model to predict videos
def init_model():
	global videoPath, outputPath, model_loaded, netMain, metaMain, altNames, socketio_event_count

	# E:/Projects/skripsi/alexeyb_darknet_cuda_working_by_vs/build/darknet/x64/
	# config for yolov4 model
	# configPath = "./cfg/yolov4.cfg"
	# weightPath = "./Models/yolov4.weights"
	# metaPath = "./cfg/coco.data"

	metaPath = "./Dataset/Crowdhuman/yolo_crowdhuman.data"	
	
	configPath = "./cfg/yolov4-custom-crowdhuman-tf-6.cfg"
	weightPath = "./trained/yolov4/Training_9_[28_04_2021]/yolov4-custom-crowdhuman-tf-6_best.weights"
	
	# configPath = "./cfg/yolov4-custom-crowdhuman-tf-5.cfg"
	# weightPath = "./trained/yolov4/Training_7_[26_04_2021]/yolov4-custom-crowdhuman-tf-5_best.weights"
	
	# configPath = "./cfg/yolov4-custom-crowdhuman-tf-4.cfg"
	# weightPath = "./trained/yolov4/Training_8_[25_04_2021]/yolov4-custom-crowdhuman-tf-4_best_7.weights"
	
	# configPath = "./cfg/yolov4-custom-crowdhuman-tf-3.cfg"
	# weightPath = "./trained/yolov4/Training_6_[25_04_2021]/yolov4-custom-crowdhuman-tf-3_best.weights"
	
	# configPath = "./cfg/yolov4-custom-crowdhuman-tf-7.cfg"
	# weightPath = "./trained/yolov4/Training_10_[03_05_2021]/yolov4-custom-crowdhuman-tf-7_best.weights"
	
	# configPath = "./cfg/yolov4-custom-crowdhuman-tf-2.cfg"
	# weightPath = "./trained/yolov4/Training_5_[25_04_2021]/yolov4-custom-crowdhuman-tf-2_best.weights"
	
	# configPath = "./cfg/yolov4-custom-crowdhuman-tf-1.cfg"
	# weightPath = "./trained/yolov4/Training_4_[24_04_2021]/yolov4-custom-crowdhuman-tf-1_best.weights"
	
	# configPath = "./cfg/yolov4-custom-crowdhuman-3.cfg"
	# weightPath = "./trained/yolov4/Training_3_[21_04_2021]/yolov4-custom-crowdhuman-3_best.weights"
	
	# configPath = "./cfg/yolov4-custom-crowdhuman-2.cfg"
	# weightPath = "./trained/yolov4/Training_2_[17_04_2021]/yolov4-custom-crowdhuman-2_best.weights"
	
	# configPath = "./cfg/yolov4-custom-crowdhuman-1.cfg"
	# weightPath = "./trained/yolov4/Training_1_[23_03_2021]/yolov4-custom-crowdhuman-1_12000_best.weights"
	
	# configPath = "./cfg/custom-yolov4-detector.cfg"
	# weightPath = "./trained/yolov4/Training_0_[23_03_2021]/custom-yolov4-detector_best.weights"
	
	# configPath = "./cfg/yolov4-custom-crowdhuman-vgg16-3.cfg"
	# weightPath = "./trained/vgg16-yolov4/yolov4-custom-crowdhuman-vgg16-3_best.weights"
	
	# configPath = "./cfg/yolov4-tiny-custom-crowdhuman-1.cfg"
	# weightPath = "./trained/yolov4_tiny/Training_1_[30_03_2021]/yolov4-tiny-custom-crowdhuman-1_best.weights"
	
	# configPath = "./cfg/yolov4-tiny-custom-crowdhuman-2.cfg"
	# weightPath = "./trained/yolov4_tiny/Training_2_[22_04_2021]/yolov4-tiny-custom-crowdhuman-2_best.weights"
	
	# configPath = "./cfg/yolov4-tiny-custom-crowdhuman-3.cfg"
	# weightPath = "./trained/yolov4_tiny/Training_3_[23_04_2021]/yolov4-tiny-custom-crowdhuman-3_best.weights"
	
	# configPath = "./cfg/yolov4-tiny-custom-crowdhuman-4.cfg"
	# weightPath = "./trained/yolov4_tiny/Training_4_[24_04_2021]/yolov4-tiny-custom-crowdhuman-4_best_13.weights"
	
	if not os.path.exists(configPath):
		raise ValueError("Invalid config path `" +
						os.path.abspath(configPath)+"`")
	if not os.path.exists(weightPath):
		raise ValueError("Invalid weight path `" +
						os.path.abspath(weightPath)+"`")
	if not os.path.exists(metaPath):
		raise ValueError("Invalid data file path `" +
						os.path.abspath(metaPath)+"`")
	if netMain is None:
		netMain = darknet.load_net_custom(configPath.encode(
			"ascii"), weightPath.encode("ascii"), 0, 1)  # batch size = 1
	if metaMain is None:
		metaMain = darknet.load_meta(metaPath.encode("ascii"))
	if altNames is None:
		try:
			with open(metaPath) as metaFH:
				metaContents = metaFH.read()
				import re
				match = re.search("names *= *(.*)$", metaContents,
								re.IGNORECASE | re.MULTILINE)
				if match:
					result = match.group(1)
				else:
					result = None
				try:
					if os.path.exists(result):
						with open(result) as namesFH:
							namesList = namesFH.read().strip().split("\n")
							altNames = [x.strip() for x in namesList]
				except TypeError:
					pass
		except Exception:
			pass
	model_loaded = True
	# broadcast message that model has been loaded
	socketio.emit('model_loaded', namespace='/detect', broadcast=True)
	socketio_event_count += 1
	print('sent event to socket io: ', socketio_event_count)

# parse arguments got from command line
def parse_arguments():
	global url
	# construct the argument parser and parse command line arguments
	# required=True for mandatory params
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", type=str, nargs="?", const="127.0.0.1",
		help="ip address of the device")
	ap.add_argument("-o", "--port", type=int, nargs="?", const="8000",
		help="ephemeral port number of the server (1024 to 65535)")
	ap.add_argument("-f", "--frame-count", type=int, default=32,
		help="# of frames used to construct the background model")
	
	args = vars(ap.parse_args())
	ip = str(args["ip"]) if (args["ip"] is not None) else "127.0.0.1"
	port = str(args["port"]) if (args["port"] is not None) else "8000"
	url = 'http://' + ip + ':' + port
	
	return args

# read video, triggered when detect_video starts up
def read_video():
	global vs, videoPath
	# 
	vs = FileVideoStream(videoPath, 1280, 720).start()
	# vs.start()
	print("after changing:", vs.stream.get(3), vs.stream.get(4))
	# time.sleep(3)

	# returns frame, width, height, fps
	return vs, vs.stream.get(3), vs.stream.get(4), vs.stream.get(cv2.CAP_PROP_FPS)

# serve web
def serve_web(args):
	# start the flask app
	# app.run(host=args["ip"], port=args["port"], debug=True,
	# 	threaded=True, use_reloader=False)
	socketio.run(app, host=args["ip"] or '127.0.0.1', 
				port=args["port"] or 8000,
				debug=True,
				use_reloader=False
			)

# check to see if this is the main thread of execution
if __name__ == '__main__':
	
	# global url
	args = parse_arguments()
	serve_web(args)
