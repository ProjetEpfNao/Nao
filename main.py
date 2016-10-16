from commands.nao import Nao
from client.client import Client
import requests

if __name__ == "__main__":
    #TODO: Add argv options for ip/host
    robot = Nao()
    client = Client(robot, requests.Session)
    client.start()
