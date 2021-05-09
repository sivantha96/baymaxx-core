import json
import vosk
import pyttsx3
import requests
from threading import Thread
import os
import queue
import sounddevice as sd
import sys

from environment import Environment

CHUNK = 8000  # number of data points to read at a time

device_info = sd.query_devices(sd.default.device, 'input')
sample_rate = int(device_info['default_samplerate'])  # sample rate of the microphone
device = sd.default.device  # microphone device
rawAudioQueue = queue.Queue()  # queue to hold raw audio chunks


# callback to save each audio chunk in a queue
def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    rawAudioQueue.put(bytes(indata))


# rasa chatbot server
def start_rasa_server():
    os.system("rasa run")


# rasa action server
def start_rasa_action_server():
    os.system("rasa run actions")


class Conversation:
    def __init__(self, mongo):
        if not os.path.exists("model"):
            print("Please download a model for your language from https://alphacephei.com/vosk/models")
            print("and unpack as 'model' in the root folder.")

        model = vosk.Model("model")

        self.mongo = mongo
        self.recognizer = vosk.KaldiRecognizer(model, sample_rate)
        self.voice_engine = pyttsx3.init()
        print("Conversation Engine configured")

    def start_listening(self):
        print('listening...')

        with sd.RawInputStream(samplerate=sample_rate, blocksize=CHUNK, device=device, dtype='int16',
                               channels=1, callback=callback):

            while True:
                data = rawAudioQueue.get()
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    if len(result['text']):
                        payload = {'message': result['text']}
                        responses = requests.post('http://localhost:5000/chat',
                                                  data=json.dumps(payload)).json()
                        if len(responses) != 0:
                            for res in responses:
                                if len(res['text']) != 0:
                                    print("Chatbot - ", res['text'])

    def start(self):
        rasa_server = Thread(target=start_rasa_server)
        rasa_action_server = Thread(target=start_rasa_action_server)
        listener = Thread(target=self.start_listening)

        rasa_server.start()
        rasa_action_server.start()
        listener.start()

        rasa_server.join()
        rasa_action_server.join()
        listener.join()
        print("Conversation Engine started")
