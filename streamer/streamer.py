import os
import threading
import requests
import time

MAX_SKIP_DELAY = 10


class Streamer(object):

    def __init__(self, server_url, paths, max_skip_delay=MAX_SKIP_DELAY):
        self.is_running = False
        self.max_skip_delay = max_skip_delay
        self.paths = paths
        self.server_url = server_url
        print("Streamer initiated.")

    def delete_file(self, path):
        print("Deleting", path)
        os.remove(path)

    def delete_files(self, paths):
        for p in paths:
            self.delete_file(p)

    def get_next_path(self, paths):
        if len(paths) == 0:
            return None
        if len(paths) < self.max_skip_delay:
            return paths.pop(0)
        # if we're too far behind, skip them all up to the last
        self.delete_files(paths[:-1])
        path = paths.pop(-1)
        del paths[:]
        return path

    def stream_file(self, file):
        files = {'file': file}
        requests.post(self.server_url, files=files)

    def run(self):
        while self.is_running:
            path = self.get_next_path(self.paths)
            if path == None:
                time.sleep(0.2)
                continue
            print("Streaming:", path)
            with open(path, "rb") as f:
                self.stream_file(f)
            print("Done streaming:", path)
            self.delete_file(path)
            time.sleep(0.1)

    def start(self):
        self.is_running = True
        threading.Thread(target=self.run).start()
        print("Streamer started.")

    def stop(self):
        self.is_running = False
