from password_manager import PasswordManager
from client_exception import ConnectionError
import rest_api


class Client(object):
    "Object in charge of communicating to the server, sending status info and fetching commands."

    def __init__(self, Session):
        "Creates a new client and attempts to authenticate to the server."
        self.session = Session()
        self.password_manager = None

    def start(self):
        "Loads credentials and authenticates with the server."
        self.init_password_manager()
        self.authenticate()

    def init_password_manager(self):
        "Creates a password manager and loads or fetches credentials."
        self.password_manager = PasswordManager()
        try:
            self.password_manager.load()
        except IOError:
            user, passwd = self.fetch_new_credentials()
            self.password_manager.save(user, passwd)

    def fetch_new_credentials(self):
        "Fetches a new username/password pair from the server, creating a robot object on it by doing so."
        resp = self.session.get(rest_api.CREDENTIALS_URL)
        if resp.status_code != 200:
            raise ConnectionError(resp.status_code)
        data = resp.json()
        return (data[rest_api.CRED_USER_KEY], data[rest_api.CRED_PASS_KEY])

    def authenticate(self):
        pass

if __name__ == "__main__":
    import requests
    Client(requests.Session)
