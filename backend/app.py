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
ar = None
art = None
cx = 0
cy = 0
xrang = 1280
yrang = 800
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
	global person
	global vr
	global vrt
	global ar
	global art
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
	audio_path = os.path.join(dir_name, "audio.wav")
	position_path = os.path.join(dir_name, "position.txt")

	vr = record.VideoRecorder(brightness, contrast, saturation, hue, gain, exposure, gamma, backlight, temperature, sharpness)
	vrt = threading.Thread(target = vr.run, args=(video_path,))
	vrt.start()

	ar = record.AudioRecorder()
	art = threading.Thread(target = ar.run, args=(audio_path,))
	art.start()

	f = open(position_path, "w")
	f.write(str(cx) + " " + str(cy))

def stop_record(stage, task, count):
	global vr
	global vrt
	global ar
	global art
	vr.terminate()
	ar.terminate()

	vrt.join()
	art.join()


def load_pipeline():
	f = open("pipeline.txt", "r", encoding='utf-8')
	lines = f.readlines()
	for line in lines:
		segs = line.split(',')
		pipeline.append({
			'stage': int(segs[0]),
			'task': int(segs[1]),
			'count': int(segs[2]),
			'title': segs[3],
			'message': segs[4]
		})

def generate_coord():
	global xrang
	global yrang
	x = random.randint(1, xrang - 300)
	y = random.randint(1, yrang - 300)
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
	return jsonify([])

@app.route('/end', methods = ['POST'])
def end():
	global cx
	global cy
	stage = int(request.json['stage'])
	task = int(request.json['task'])
	count = int(request.json['count'])
	print('end', stage, task, count)
	if stage > 0:
		stop_record(stage, task, count)
	result = get_next_task(stage, task, count)
	cx = result['x']
	cy = result['y']
	return jsonify(result)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--width', '-w')
	parser.add_argument('--height', '-e')
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
	xrang = int(args.width)
	yrang = int(args.height)
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
