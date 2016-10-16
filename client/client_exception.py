

class ClientException(Exception):
    pass


class ConnectionError(ClientException):
    pass


class NoSuchCommandError(ClientException):
    pass
