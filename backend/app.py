#-*- encoding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import copy
import record
import random
import threading
import argparse

app = Flask(__name__)
CORS(app, supports_credentials=True)

pipeline = []

person = {
	"name": "test",
	"sid": "",
	"age": 0,
	"is_right": True
}

vr = None
vrt = None
cx = 0
cy = 0
width = 1600
height = 800
brightness = 0
contrast = 0
saturation = 0
hue = 0
gain = 0
exposure = 0
gamma = 0
backlight = 0
temperature = 0
sharpness = 0

def start_record(stage, task, count):
	global width
	global height
	global person
	global vr
	global vrt
	global cx
	global cy
	global brightness
	global contrast
	global saturation
	global hue
	global gain
	global exposure
	global gamma
	global backlight
	global temperature
	global sharpness
	dir_name = os.path.join("data", str(person["name"]) + "_" + str(person["sid"]), str(stage), str(task), str(count))
	try:
		os.makedirs(dir_name)
	except:
		pass

	video_path = os.path.join(dir_name, "video.avi")
	position_path = os.path.join(dir_name, "position.txt")

	vr = record.VideoRecorder(width, height, brightness, contrast, saturation, hue, gain, exposure, gamma, backlight, temperature, sharpness)
	vrt = threading.Thread(target = vr.run, args=(video_path,))
	vrt.start()

	f = open(position_path, "w")
	f.write(str(cx) + " " + str(cy))

def stop_record(stage, task, count):
	global vr
	global vrt
	vr.terminate()
	vrt.join()


def load_pipeline():
	f = open("pipeline.txt", "r", encoding='utf-8')
	lines = f.readlines()
	for line in lines:
		segs = line.split(',')
		pipeline.append({
			'stage': int(segs[0]),
			'task': int(segs[1]),
			'count': int(segs[2]),
			'time': int(segs[3]),
			'title': segs[4],
			'message': segs[5]
		})

def generate_coord():
	global width
	global height
	x = random.randint(1, width - 300)
	y = random.randint(1, height - 300)
	return x, y

def get_next_task(stage, task, count):
	x, y = generate_coord()
	for i in range(len(pipeline)):
		p = pipeline[i]
		if p['stage'] == stage and p['task'] == task:
			if count == p['count']: # next stage
				if i + 1 == len(pipeline):
					return {}
				else:
					res = copy.deepcopy(pipeline[i + 1])
					res['count'] = 1
					res['remain'] = pipeline[i + 1]['count'] - res['count'] + 1
					res['x'] = x
					res['y'] = y
					res['hascross'] = '叉号' in res['message']
					return res
			else:
				res = copy.deepcopy(pipeline[i])
				res['count'] = count + 1
				res['remain'] = pipeline[i]['count'] - res['count'] + 1
				res['x'] = x
				res['y'] = y
				res['hascross'] = '叉号' in res['message']
				return res
	return {}

def get_time(stage, task):
	for i in range(len(pipeline)):
		if pipeline[i]['stage'] == stage and pipeline[i]['task'] == task:
			return pipeline[i]['time']
	return 30

@app.route('/login', methods = ['POST'])
def login():
	global person
	name = request.json['name']
	sid = request.json['sid']
	age = int(request.json['age'])
	is_right = request.json['is_right'] == 'true'
	person = {
		"name": name,
		"sid": sid,
		"age": age,
		"is_right": is_right
	}
	return "ok"

@app.route('/begin', methods = ['POST'])
def begin():
	stage = int(request.json['stage'])
	task = int(request.json['task'])
	count = int(request.json['count'])
	print('begin', stage, task, count)
	if stage > 0:
		start_record(stage, task, count)
	return jsonify({'time': get_time(stage, task)})

@app.route('/end', methods = ['POST'])
def end():
	global cx
	global cy
	stage = int(request.json['stage'])
	task = int(request.json['task'])
	count = int(request.json['count'])
	first = int(request.json['first'])
	print(first)
	print('end', stage, task, count)
	if first == 0:
		stop_record(stage, task, count)
	result = get_next_task(stage, task, count)
	cx = result['x']
	cy = result['y']
	return jsonify(result)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--width', '-w', default=1280)
	parser.add_argument('--height', '-e', default=1024)
	parser.add_argument('--brightness', default=29)
	parser.add_argument('--contrast', default=40)
	parser.add_argument('--saturation', default=30)
	parser.add_argument('--hue', default=-23)
	parser.add_argument('--gain', default=55)
	parser.add_argument('--exposure', default=25)
	parser.add_argument('--gamma', default=121)
	parser.add_argument('--backlight', default=1)
	parser.add_argument('--temperature', default=4690)
	parser.add_argument('--sharpness', default=2)

	args = parser.parse_args()
	width = int(args.width)
	height = int(args.height)
	brightness = int(args.brightness)
	contrast = int(args.contrast)
	saturation = int(args.saturation)
	hue = int(args.hue)
	gain = int(args.gain)
	exposure = int(args.exposure)
	gamma = int(args.gamma)
	backlight = int(args.backlight)
	temperature = int(args.temperature)
	sharpness = int(args.sharpness)

	load_pipeline()
	app.run(host='0.0.0.0')
