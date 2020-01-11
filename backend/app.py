#-*- encoding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import os
import copy

app = Flask(__name__)
CORS(app, supports_credentials=True)

pipeline = []

person = {
    "name": "test",
    "sid": "",
    "age": 0,
    "is_right": True
}

def start_record(stage, task, count):
    global person
    dir_name = "data/" + str(person["name"]) + "/" + str(stage) + "/" + str(task) + "/" + str(count)
    try:
        os.mkdirs(dir_name)
    except:
        pass
    # record video
    video_path = dir_name + "/video.avi"

    # record audio
    audio_path = dir_name + "/audio.wav"

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
    x = random.randint(1, 600)
    y = random.randint(1, 600)
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
                    return res
            else:
                res = copy.deepcopy(pipeline[i])
                res['count'] = count + 1
                res['remain'] = pipeline[i]['count'] - res['count'] + 1
                res['x'] = x
                res['y'] = y
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
    result = get_next_task(stage, task, count)
    start_record(stage, task, count)
    print(result)
    return jsonify(result)

@app.route('/end', methods = ['POST'])
def end():
    return jsonify([])


if __name__ == '__main__':
    load_pipeline()
    app.run(host='0.0.0.0')
