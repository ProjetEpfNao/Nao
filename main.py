from commands.nao import Nao
from client.client import Client
from streamer.streamer import Streamer
from commands.stream_feeder import StreamFeeder
import requests
import time


if __name__ == "__main__":
    IP = "localhost"
    PORT = 9559
    REMOTE = "http://54.173.164.98:80/upload"

    # TODO: Add argv options for ip/host
    robot = Nao(IP, PORT)
    client = Client(robot, requests.Session)
    client.start()

    feed = StreamFeeder(IP, PORT)
    feed.start()

    streamer = Streamer(REMOTE, feed.recordings)
    streamer.start()

    # To exit cleanly on keyboard interrupts.
    i = 0  # Safeguard in case I lose connection to robot and can't shutdown stream, don't want to saturate hard-drive

    try:
        while 1:
            time.sleep(1)
            i += 1
            if i > 100:
                pass
                #break
    except:
        pass

    client.stop()
    feed.stop()
    # Giving time for streamer to finish putting his things in order
    time.sleep(4)
    streamer.stop()
