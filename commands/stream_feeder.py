import uuid
import os

RECORIDNG_LENGTH = 4
RECORDING_PATH = "/var/persistent/recordings"


class StreamFeeder(object):

    def __init__(self, ip, port, recording_path=RECORDING_PATH,
                 recording_length=RECORIDNG_LENGTH):
        self.recording_path = recording_path
        self.recording_length = recording_length
        self.recordings = []
        self.is_recording = False
        self.configure()

    def configure(self):
        # Configure video format
        self.vr = ALProxy("ALVideoRecorder", IP, PORT)
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
        path = os.path.join(self.recording_path, filename)
        self.recordings.append(path)

    def record_continuously(self):
        while self.is_recording:
            self.record_video()

    def start(self):
        self.is_recording = True
        threading.Thread(target=self.record_continuously).start()

    def stop(self):
        self.is_recording = False
