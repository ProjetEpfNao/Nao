import time
from shutil import copyfile
import uuid

def feed(paths):
    while 1:
        new_path = str(uuid.uuid4()) + ".avi"
        copyfile(PATH, new_path)
        paths.append(new_path)
        time.sleep(DELAY)

if __name__ == "__main__":
    PATH = "..\\stream_data\\test.avi"
    DELAY = 15
    REMOTE = "http://54.152.73.101:80/upload"
    #REMOTE = "http://localhost:80/upload"

    import os
    import sys
    abs_path = os.path.abspath("..\\..")
    print(abs_path)
    sys.path.append(abs_path)

    from Nao.streamer import streamer

    paths = []
    s = streamer.Streamer(REMOTE, paths)
    s.start()

    try:
        feed(paths)
    except: #To deal with keyboard interrupt
        print(sys.exc_info())

    s.stop()
