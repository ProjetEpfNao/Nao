from naoqi import ALProxy

HOST = "localhost"
PORT = 9559


class Nao(object):

    def __init__(self, ip=HOST, port=PORT):
        self.ip = ip
        self.port = port
        self.commands = dir(self)

    def execute(self, command_string, *args):
        self.commands[command_string](*args)

    def reply(self, *args):
        print(args)

    def has_command(self, command_string):
        return command_string in self.commands

    def set_command_callback(self, callback):
        self.reply = callback

    def stand_up(self):
        tts = ALProxy("ALTextToSpeech", self.ip, self.port)
        motion = ALProxy("ALMotion", self.ip, self.port)
        if motion.robotIsWakeUp():
            motion.rest()
        else:
            motion.wakeUp()
            tts.say("Bonjour Roman.")


if __name__ == "__main__":
    nao = Nao()
    nao.stand_up()
