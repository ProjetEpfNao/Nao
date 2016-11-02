import time
import threading

THREAD_DELAY = 0.01

class Streamer(object):

    def __init__(self, feed, session, url, thread_delay=THREAD_DELAY):
        self.feed = feed
        self.session = session
        self.url = url

    def start(self):
        self.run = True
        t = threading.Thread(target=self.stream)
        t.start()

    def stop(self):
        self.run = False

    def post_next_frame(self):
        frame = self.feed.get_next_frame()
        if frame:
            data = frame.get_data()
            self.session.post(self.url, data=data)

    def stream(self):
        while self.run:
            self.post_next_frame()
            time.sleep(self.thread_delay)
