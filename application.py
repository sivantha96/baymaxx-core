import os
from multiprocessing import Process, Value
from threading import Thread

from engines.conversation import Conversation
from engines.video import Video
from engines.control import Control

from flask import Flask, request
from flask_pymongo import PyMongo

from environment import Environment

application = Flask(__name__)
application.config["MONGO_URI"] = Environment.LOCAL_DB
mongo = PyMongo(application)

conversation = Conversation(mongo)
video = Video(mongo)
control = Control(mongo)


@application.route('/')
def hello_world():
    return 'Hello, World!'

@application.route('/chat', methods=['POST'])
def chat():
    print('here')
    data = request.get_json()
    user = video.get_current_user()
    print(user)
    return 'Hello, World!'


def start_engines(bot_state, is_face_detected):
    control_engine = Thread(target=control.start, args=(1, bot_state, is_face_detected, 50))
    video_engine = Thread(target=video.start)
    conversation_engine = Thread(target=conversation.start)

    control_engine.start()
    video_engine.start()
    conversation_engine.start()

    control_engine.join()
    video_engine.join()
    conversation_engine.join()


def start_api(bot_state, is_face_detected):
    # flask server
    application.run()


if __name__ == "__main__":
    # globals
    global is_face_detected
    is_face_detected = Value('d')
    is_face_detected.value = 0

    global bot_state
    bot_state = Value('d')
    bot_state.value = 1

    engines = Process(target=start_engines, args=(bot_state, is_face_detected))
    api = Process(target=start_api, args=(bot_state, is_face_detected))

    engines.start()
    api.start()

    engines.join()
    api.join()
