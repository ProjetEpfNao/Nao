from password_manager import PasswordManager
from client_exception import ConnectionError, NoSuchCommandError, ServerError
from command import Command
import rest_api
import threading
import time
import uuid
import sys


class Client(object):
    "Object in charge of communicating to the server, sending status info and fetching commands."

    def __init__(self, robot, Session):
        "Creates a new client and attempts to authenticate to the server."
        self.robot = robot
        self.robot.set_command_callback(self.send_command_reply)
        self.session = Session()
        self.password_manager = None
        self.keep_running = False
        self.command_queue = []

    def start(self):
        "Loads credentials and authenticates with the server."
        self.init_password_manager()
        self.authenticate()
        threading.Thread(target=self.poll).start()

    def stop(self):
        "Stops polling the server."
        self.keep_running = False

    def execute_on_robot(self, command_string, *args):
        "Executes a command on the robot if it exists, raises an error otherwise."
        if not self.robot.has_command(command_string):
            error_message = "Command " + command_string + " not found."
            raise NoSuchCommandException(error_message)
        self.robot.execute(command_string, *args)

    def init_password_manager(self):
        "Creates a password manager and loads or fetches credentials."
        self.password_manager = PasswordManager()
        try:
            self.password_manager.load()
        except IOError:
            user, passwd = self.fetch_new_credentials()
            self.password_manager.save(user, passwd)

    def fetch_data(self, url):
        "Gets the given url and returns a json object from the response body."
        resp = self.session.get(url)
        if resp.status_code != 200:
            raise ConnectionError(resp.status_code)
        body = resp.json()
        if body[rest_api.STATUS_KEY] == rest_api.FAILURE:
            raise ServerError(body[rest_api.ERROR_KEY])
        return body

    def fetch_new_credentials(self):
        "Fetches a new username/password pair from the server, creating a robot object on it by doing so."
        data = self.fetch_data(rest_api.CREDENTIALS_URL)
        return (data[rest_api.CRED_USER_KEY], data[rest_api.CRED_PASS_KEY])

    def authenticate(self):
        pass

    def fetch_command(self):
        "Fetches the latest command sent by the user."
        data = self.fetch_data(rest_api.COMMAND_URL)
        command_id = str(uuid.uuid4())
        command_type = data[rest_api.COMMAND_TYPE_KEY]
        if len(command_type) == 0: return None
        return Command(command_id, command_type)

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
                try:
                    self.execute_on_robot(command.type)
                except NoSuchCommandError as e:
                    print(sys.exc_info())
                    pass  # TODO: Implement logging
            time.sleep(rest_api.POLL_DELAY)
