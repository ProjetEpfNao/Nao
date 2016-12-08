


class MockRobot(object):
    def has_command(self, command):
        print("Checked for command " + command)
        return True

    def set_command_callback(self, func):
        print("Set command callback to: " + str(func))

    def execute(self, command, *args):
        print("Executed " + str(command) + " command with args: " + str(*args))

if __name__ == "__main__":
    import os
    import sys
    import time
    abs_path = os.path.abspath("..\\..")
    print(abs_path)
    sys.path.append(abs_path)

    from Nao.client import client
    import requests
    robot = MockRobot()
    client = client.Client(robot, requests.Session)
    client.start()

    try:
        while 1:
            time.sleep(1)
    except:
        print(sys.exc_info())

    client.stop()
