

class ClientException(Exception):
    "Basic exception to be raised when the client has encountered a problem."
    pass


class ConnectionError(ClientException):
    "Exception to be raised when the client was unable to perform a request."
    pass


# TODO: Figure out if it really belongs here...
class NoSuchCommandError(ClientException):
    "Exception to be raised when the client got an invalid command string from the server."
    pass


class ServerError(ClientException):
    "Exception to be raised when the server sent back a response with a failure status."
    pass
