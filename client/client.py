from password_manager import PasswordManager
from client_exception import ConnectionError
import rest_api
import requests


class Client(object):
    "Object in charge of communicating to the server, sending status info and fetching commands."

    def __init__(self):
        "Creates a new client and attempts to authenticate to the server."
        self.session = requests.Session()

        # Create a password manager to perform auth
        self.password_manager = PasswordManager()
        try:
            self.password_manager.load()
        except IOError:
            user, passwd = self.fetch_new_credentials()
            self.password_manager.save(user, passwd)

        # Fetches auth url to create auth cookie in session
        self.authenticate()

    def fetch_new_credentials(self):
        "Fetches a new username/password pair from the server, creating a robot object on it by doing so."
        resp = self.session.get(rest_api.CREDENTIALS_URL)
        if resp.status_code != 200:
            raise ConnectionError(resp.status_code)
        data = resp.json()
        return (data[resp_api.CRED_USER_KEY], data[rest_api.CRED_PASS_KEY])

    def authenticate(self):
        pass

    def send_battery_info(self, battery):
        pass

    def open_command_stream(self):
        pass

    def send_battery_info(self):
        pass

if __name__ == "__main__":
    Client()
