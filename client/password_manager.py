

class PasswordManager(object):
    "A password manager that stores a single user/pass pair and can load or save them to a file."

    SAVE_FILE_PATH = ".credentials"

    def __init__(self, save_file_path=SAVE_FILE_PATH):
        self.save_file_path = save_file_path
        self.username = None
        self.password = None

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
