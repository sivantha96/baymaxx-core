from vosk import Model, KaldiRecognizer
import pyaudio
import os
import json
from collections import namedtuple
import pyttsx3
import time
import requests
from multiprocessing import Process, Value
from threading import Thread

import speech_recognition as sr

CHUNK = 8000  # number of data points to read at a time
RATE = 44100  # time resolution of the recording device (Hz)


def speech_callback(recognizer, audio):
    print("speech callback called")
    try:
        print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def start_rasa_server():
    os.system("rasa run")


def start_rasa_action_server():
    os.system("rasa run actions")


class Conversation:
    def __init__(self, mongo):

        self.mongo = mongo
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        self.stop_listening = lambda: None

        self.recognizer = KaldiRecognizer(Model("model"), 16000)
        self.voice_engine = pyttsx3.init()
        self.stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                                             frames_per_buffer=CHUNK)  # uses default input device
        print("Conversation Engine configured")

    def custom_object_decoder(dict):
        return namedtuple('X', dict.keys())(*dict.values())

    def start_listening(self):
        print('listening...')

        while True:
            print('.', end="")
            data = self.stream.read(CHUNK)
            if len(data) == 0:
                break
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                if len(result['text']) == 0:
                    pass
                else:
                    print(result['text'])
                    payload = {'sender': '1234dsdsd', 'message': result['text']}
                    responses = requests.post('http://localhost:5005/webhooks/rest/webhook',
                                             data=json.dumps(payload)).json()
                    if len(responses) != 0:
                        for res in responses:
                            if len(res['text']) != 0:
                                self.voice_engine.say(res['text'])
                                self.voice_engine.runAndWait()



                    print('done')

    def start(self):
        print("Conversation Engine started")
        # with self.m as source:
        #     self.r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
        # self.stop_listening = self.r.listen_in_background(self.m, speech_callback)
        rasa_server = Thread(target=start_rasa_server)
        rasa_action_server = Thread(target=start_rasa_action_server)
        listener = Thread(target=self.start_listening)

        rasa_server.start()
        rasa_action_server.start()
        listener.start()

        rasa_server.join()
        rasa_action_server.join()
        listener.join()
