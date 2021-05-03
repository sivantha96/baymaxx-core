import time
from pycreate2 import Create2

# port that the pc communicate with the base
# device manager -> COM ports -> USB serial port
port = "COM6"


class Control:
    def __init__(self, mongo):
        self.mongo = mongo
        # self.bot = Create2(port)
        # self.bot.start()
        # self.bot.full()  # full / safe / passive / off
        print("Control Engine configured")

    def pump_in_air(self):
        time.sleep(5)

    def pump_out_air(self):
        time.sleep(5)

    def start(self, thread_id, bot_state, is_face_detected, rotation_speed):
        print("Control Engine started")
        # while bot_state.value == 1:
        #     if is_face_detected.value == 1:
        #         self.bot.drive_stop()
        #     else:
        #         self.bot.drive_direct(rotation_speed * -1, rotation_speed)
