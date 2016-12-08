import rest_api


class Command(object):
    "A command gotten from the server. It has a unique id and a type."

    def __init__(self, command_id, command_type, command_content=None):
        self.id = command_id
        self.type = command_type
        self.content = command_content

    def get_post_data(self):
        data = {rest_api.COMMAND_ID_KEY: self.id, rest_api.COMMAND_TYPE_KEY: self.type}
        if self.content:
            data[rest_api.COMMAND_CONTENT_KEY] = self.content
        return data
