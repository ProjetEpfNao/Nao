try:
    from naoqi import ALProxy
except ImportError:
    # TODO: Replace this crap with environnement variable check for TEST or
    # DEV modes
    ALProxy = None
    print("Naoqi was not found, most functionnalities will not run.")
import uuid
import os
import time
import threading

RECORIDNG_LENGTH = 4
RECORDING_PATH = "/home/nao/recordings/cameras"


class StreamFeeder(object):

    def __init__(self, ip, port, recording_path=RECORDING_PATH,
                 recording_length=RECORIDNG_LENGTH):
        self.ip = ip
        self.port = port
        self.recording_path = recording_path
        self.recording_length = recording_length
        self.recordings = []
        self.is_recording = False
        self.configure()

    def configure(self):
        # Configure video format
        self.vr = ALProxy("ALVideoRecorder", self.ip, self.port)
        self.vr.setResolution(1)
        self.vr.setFrameRate(10)
        self.vr.setVideoFormat("MJPG")

    def record_video(self):
        # Record video to file
        filename = str(uuid.uuid4())
        self.vr.startRecording(self.recording_path, filename)
        time.sleep(self.recording_length)
        self.vr.stopRecording()

        # Add to recordings list
        path = os.path.join(self.recording_path, filename + ".avi")
        self.recordings.append(path)

    def record_sound(self):
        pass

    def record_continuously(self):
        while self.is_recording:
            self.record_video()

    def start(self):
        self.is_recording = True
        threading.Thread(target=self.record_continuously).start()

    def stop(self):
        self.is_recording = False



if __name__ == "__main__":
    IP = "localhost"
    PORT = 9559
    feed = StreamFeeder(IP, PORT)
    feed.record_video()
