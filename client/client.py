from password_manager import PasswordManager
from client_exception import ConnectionError, NoSuchCommandError, ServerError
from command import Command
import rest_api
import threading
import time
import uuid
import sys


class Client(object):  # TODO: Add high level error handling and output to robot voice
    "An object in charge of communicating with the server, sending status info and fetching commands."

    def __init__(self, robot, Session):
        "Creates a new client and attempts to authenticate to the server."
        self.robot = robot
        self.robot.set_command_callback(self.send_command_reply)
        self.session = Session()
        self.password_manager = None
        self.keep_running = False
        self.command_queue = []
        print("Client initiated.")

    def start(self):
        "Loads credentials and authenticates with the server."
        self.init_password_manager()
        creds = self.password_manager.get_credentials()
        self.login(*creds)
        threading.Thread(target=self.poll).start()
        print("Client started.")

    def stop(self):
        "Stops polling the server."
        self.keep_running = False

    def execute_on_robot(self, command_string, *args):
        "Executes a command on the robot if it exists, raises an error otherwise."
        if not self.robot.has_command(command_string):
            error_message = "Command " + command_string + " not found."
            raise NoSuchCommandError(error_message)
        result = self.robot.execute(command_string, *args)

        if command_string == "battery":  # ugly but whatever
            self.post_battery_info(result)

    def init_password_manager(self):
        "Creates a password manager and loads or fetches credentials."
        self.password_manager = PasswordManager()
        try:
            self.password_manager.load()
            print("Loaded credentials.")
        except IOError:
            user, passwd = self.password_manager.gen_credentials()
            self.register(user, passwd)
            self.password_manager.save(user, passwd)
            print("Generated new credentials.")

    def parse_response(self, resp):
        if resp.status_code != 200:
            raise ConnectionError(resp.status_code)
        body = resp.json()
        if body[rest_api.STATUS_KEY] == rest_api.FAILURE:
            raise ServerError(body[rest_api.ERROR_KEY])
        return body

    def fetch_data(self, url):  # TODO: replace this fetch and only this one with get
        "Gets the given url and returns a json object from the response body."
        resp = self.session.get(url)
        return self.parse_response(resp)

    def post_data(self, url, data):
        "Posts data to the given url and returns a  json object from the response body."
        resp = self.session.post(url, data=data)
        return self.parse_response(resp)

    def post_battery_info(self, battery):
        data = {rest_api.BATTERY_KEY: battery}
        return self.post_data(rest_api.BATTERY_URL, data)

    def register(self, username, password):
        "Generates a new username/password pair and register on the server."
        creds = {rest_api.USER_KEY: username,
                 rest_api.PASS_KEY: password, rest_api.ROBOT_KEY: True}
        self.post_data(rest_api.REGISTER_URL, data=creds)

    def login(self, username, password):
        creds = {rest_api.USER_KEY: username, rest_api.PASS_KEY: password}
        self.post_data(rest_api.LOGIN_URL, data=creds)

    def fetch_command(self):
        "Fetches the latest command sent by the user."
        data = self.fetch_data(rest_api.COMMAND_URL)
        command_id = str(uuid.uuid4())
        command_type = data[rest_api.COMMAND_TYPE_KEY]
        command_content = None
        if rest_api.COMMAND_CONTENT_KEY in data:
            command_content = data[rest_api.COMMAND_CONTENT_KEY]
        if len(command_type) == 0:
            return None
        return Command(command_id, command_type, command_content)

    def send_command_reply(self, command, reply_data):
        "Sends a reply for the given command."
        reply = command.get_post_dict()
        reply[rest_api.REPLY_DATA_KEY] = reply_data
        self.session.post(rest_api.REPLY_URL, data=reply)

    def poll(self):
        "Regularly polls the server for new commands until told to stop."
        self.keep_running = True
        while self.keep_running:
            command = self.fetch_command()
            if command:
                args = []
                if command.content:
                    args = [command.content]
                try:
                    print("Received new command.", command.type)
                    self.execute_on_robot(command.type, *args)
                except NoSuchCommandError as e:
                    print(sys.exc_info())
                    pass  # TODO: Implement logging
            time.sleep(rest_api.POLL_DELAY)
