import os
import base64

class PasswordManager(object):
    "A password manager that stores a single user/pass pair and can load or save them to a file."

    SAVE_FILE_PATH = ".credentials"

    def __init__(self, save_file_path=SAVE_FILE_PATH):
        self.save_file_path = save_file_path
        self.username = None
        self.password = None

    def gen_random_string(self):
        random_bytes = os.urandom(32)
        return base64.b64encode(random_bytes)[:32] #TODO: constant

    def gen_credentials(self):
        username = self.gen_random_string()
        password = self.gen_random_string()
        return (username, password)

    def get_credentials(self):
        return (self.username, self.password)

    def save(self, username, password):
        "Saves the stored username/password pair to the default file."
        self.username = username
        self.password = password
        with open(self.save_file_path, "w") as f:
            f.write(self.username + "\n" + self.password)

    def load(self):
        "Loads a username/password pair from the default file."
        with open(self.save_file_path, "r") as f:
            data = f.read()
        self.username, self.password = data.split("\n")
