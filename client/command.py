import rest_api


class Command(object):

    def __init__(self, command_id, command_type):
        self.id = command_id
        self.type = command_type

    def get_post_data(self):
        return {rest_api.COMMAND_ID_KEY: self.id, rest_api.COMMAND_TYPE_KEY: self.type}
