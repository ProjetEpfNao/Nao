try:
    from naoqi import ALProxy
except ImportError:
    ALProxy = None
    print("Naoqi was not found, most functionnalities will not run.")
import time


class Nao(object):
    "A Nao robot that can execute commands and report its status."

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.commands = {"stand_up": self.toggle_stand,  # TODO: update command name after demo
                         "sit_down": self.sit_down,
                         "raise_arm": self.raise_arm,
                         "look_up": self.look_up,
                         "look_down": self.look_down,
                         "look_left": self.look_left,
                         "look_right": self.look_right,
                         "battery": self.get_battery,
                         "speak": self.speak,
                         "volume_up": self.volume_up,
                         "volume_down": self.volume_down}

    def execute(self, command_string, *args):
        "Execute a command by its name."
        return self.commands[command_string](*args)

    def reply(self, *args):
        "Reply callback that'll be called when a command is completed."
        print(args)

    def has_command(self, command_name):
        "Returns true if the command with the given name exists."
        return command_name in self.commands

    def set_command_callback(self, callback):
        "Overrides the reply function that'll be called upon completion of a command."
        self.reply = callback

    def toggle_stand(self):
        "Makes the robot stand if it's sitting, makes him sit otherwise."
        # tts = ALProxy("ALTextToSpeech", self.ip, self.port)
        motion = ALProxy("ALMotion", self.ip, self.port)
        if motion.robotIsWakeUp():
            motion.rest()
        else:
            motion.wakeUp()

    def sit_down(self):
        "Makes the robot stand if it's sitting, makes him sit otherwise."
        # tts = ALProxy("ALTextToSpeech", self.ip, self.port)
        motion = ALProxy("ALMotion", self.ip, self.port)
        if motion.robotIsWakeUp():
            motion.rest()

    def look_up(self):
        try:
            motion = ALProxy("ALMotion", self.ip, self.port)
            motion.setStiffnesses("Head", 1.0)
            names = "HeadPitch"
            changes = -0.15
            fractionMaxSpeed = 0.05
            motion.changeAngles(names, changes, fractionMaxSpeed)
        except BaseException, err:
            print err

    def look_down(self):
        try:
            motion = ALProxy("ALMotion", self.ip, self.port)
            motion.setStiffnesses("Head", 1.0)
            names = "HeadPitch"
            changes = 0.15
            fractionMaxSpeed = 0.05
            motion.changeAngles(names, changes, fractionMaxSpeed)
        except BaseException, err:
            print err

    def look_right(self):
        try:
            motion = ALProxy("ALMotion", self.ip, self.port)
            motion.setStiffnesses("Head", 1.0)
            names = "HeadYaw"
            changes = -0.15
            fractionMaxSpeed = 0.05
            motion.changeAngles(names, changes, fractionMaxSpeed)
        except BaseException, err:
            print err

    def look_left(self):
        try:
            motion = ALProxy("ALMotion", self.ip, self.port)
            motion.setStiffnesses("Head", 1.0)
            names = "HeadYaw"
            changes = 0.15
            fractionMaxSpeed = 0.05
            motion.changeAngles(names, changes, fractionMaxSpeed)
        except BaseException, err:
            print err

    def get_battery(self):
        "Returns the percentage of remaining battery."
        try:
            battery = ALProxy("ALBattery", self.ip, self.port)
            return battery.getBatteryCharge()
        except BaseException, err:
            print err
            return 0

    def speak(self, tts):
        tts = tts.encode("latin1")
        print("About to say:", tts)
        try:
            altts = ALProxy("ALTextToSpeech", self.ip, self.port)
            altts.say(tts)
        except BaseException, err:
            print err

    def volume_up(self):
        try:
            audio = ALProxy("ALAudioDevice", self.ip, self.port)
            volume = audio.getOutputVolume()
            volume = volume+20
            if(volume > 100):
                audio.setOutputVolume(100)
            else:
                audio.setOutputVolume(volume)
        except BaseException, err:
            print err

    def volume_down(self):
        try:
            audio = ALProxy("ALAudioDevice", self.ip, self.port)
            volume = audio.getOutputVolume()
            volume = volume-20
            if(volume < 0):
                audio.setOutputVolume(0)
            else:
                audio.setOutputVolume(volume)
        except BaseException, err:
            print err


    def raise_arm(self):
        "Raises the robot's arm."
        names = list()
        times = list()
        keys = list()

        names.append("RElbowRoll")
        times.append(
            [0.52, 1.04, 1.52, 2.04, 2.52, 3.04, 3.52, 4.04, 4.52, 5.04, 5.52, 6.04, 6.52, 7.04, 7.52, 8.04, 8.52])
        keys.append([[0.874422, [3, -0.173333, 0], [3, 0.173333, 0]], [0.874422, [3, -0.173333, 0], [3, 0.16, 0]],
                     [0.874422, [3, -0.16, 0], [3, 0.173333, 0]
                      ], [0.874422, [3, -0.173333, 0], [3, 0.16, 0]],
                     [0.986404, [3, -0.16, 0], [3, 0.173333, 0]],
                     [0.941918, [3, -0.173333, 0.0143583], [3, 0.16, -0.0132538]],
                     [0.903568, [3, -0.16, 0.0380432], [3, 0.173333, -0.0412134]],
                     [0.704148, [3, -0.173333, 0.1489], [3, 0.16, -0.137446]],
                     [0.044528, [3, -0.16, 0.00888131],
                         [3, 0.173333, -0.00962142]],
                     [0.0349066, [3, -0.173333, 0], [3, 0.16, 0]
                      ], [0.0349066, [3, -0.16, 0], [3, 0.173333, 0]],
                     [0.0349066, [3, -0.173333, 0], [3, 0.16, 0]
                      ], [0.0349066, [3, -0.16, 0], [3, 0.173333, 0]],
                     [0.0349066, [3, -0.173333, 0], [3, 0.16, 0]
                      ], [0.0349066, [3, -0.16, 0], [3, 0.173333, 0]],
                     [0.0349066, [3, -0.173333, 0], [3, 0.16, 0]], [0.0349066, [3, -0.16, 0], [3, 0, 0]]])

        names.append("RElbowYaw")
        times.append(
            [0.52, 1.04, 1.52, 2.04, 2.52, 3.04, 3.52, 4.04, 4.52, 5.04, 5.52, 6.04, 6.52, 7.04, 7.52, 8.04, 8.52])
        keys.append([[1.21028, [3, -0.173333, 0], [3, 0.173333, 0]], [1.21028, [3, -0.173333, 0], [3, 0.16, 0]],
                     [1.21182, [3, -0.16, 0], [3, 0.173333, 0]
                      ], [1.21028, [3, -0.173333, 0], [3, 0.16, 0]],
                     [1.2379, [3, -0.16, -0.0179171], [3, 0.173333, 0.0194102]],
                     [1.32227, [3, -0.173333, -0.0252599], [3, 0.16, 0.0233168]],
                     [1.38363, [3, -0.16, -0.0311709], [3, 0.173333, 0.0337684]],
                     [1.51708, [3, -0.173333, -0.0489244], [3, 0.16, 0.0451609]],
                     [1.66588, [3, -0.16, 0], [3, 0.173333, 0]
                      ], [1.66588, [3, -0.173333, 0], [3, 0.16, 0]],
                     [1.66588, [3, -0.16, 0], [3, 0.173333, 0]
                      ], [1.66742, [3, -0.173333, 0], [3, 0.16, 0]],
                     [1.66742, [3, -0.16, 0], [3, 0.173333, 0]
                      ], [1.66588, [3, -0.173333, 0], [3, 0.16, 0]],
                     [1.66588, [3, -0.16, 0], [3, 0.173333, 0]
                      ], [1.66588, [3, -0.173333, 0], [3, 0.16, 0]],
                     [1.66588, [3, -0.16, 0], [3, 0, 0]]])

        names.append("RHand")
        times.append(
            [0.52, 1.04, 1.52, 2.04, 2.52, 3.04, 3.52, 4.04, 4.52, 5.04, 5.52, 6.04, 6.52, 7.04, 7.52, 8.04, 8.52])
        keys.append([[0.2284, [3, -0.173333, 0], [3, 0.173333, 0]], [0.2284, [3, -0.173333, 0], [3, 0.16, 0]],
                     [0.2284, [3, -0.16, 0], [3, 0.173333, 0]
                      ], [0.2284, [3, -0.173333, 0], [3, 0.16, 0]],
                     [0.2284, [3, -0.16, 0], [3, 0.173333, 0]
                      ], [0.2284, [3, -0.173333, 0], [3, 0.16, 0]],
                     [0.2284, [3, -0.16, 0], [3, 0.173333, 0]
                      ], [0.2284, [3, -0.173333, 0], [3, 0.16, 0]],
                     [0.2284, [3, -0.16, 0], [3, 0.173333, 0]
                      ], [0.2284, [3, -0.173333, 0], [3, 0.16, 0]],
                     [0.2284, [3, -0.16, 0], [3, 0.173333, 0]
                      ], [0.2284, [3, -0.173333, 0], [3, 0.16, 0]],
                     [0.2284, [3, -0.16, 0], [3, 0.173333, 0]
                      ], [0.2284, [3, -0.173333, 0], [3, 0.16, 0]],
                     [0.2284, [3, -0.16, 0], [3, 0.173333, 0]
                      ], [0.2284, [3, -0.173333, 0], [3, 0.16, 0]],
                     [0.2284, [3, -0.16, 0], [3, 0, 0]]])

        names.append("RShoulderPitch")
        times.append(
            [0.52, 1.04, 1.52, 2.04, 2.52, 3.04, 3.52, 4.04, 4.52, 5.04, 5.52, 6.04, 6.52, 7.04, 7.52, 8.04, 8.52])
        keys.append([[1.41132, [3, -0.173333, 0], [3, 0.173333, 0]], [1.41132, [3, -0.173333, 0], [3, 0.16, 0]],
                     [1.41132, [3, -0.16, 0], [3, 0.173333, 0]
                      ], [1.41132, [3, -0.173333, 0], [3, 0.16, 0]],
                     [0.865218, [3, -0.16, 0.190216], [3, 0.173333, -0.206067]],
                     [0.222472, [3, -0.173333, 0.217767], [3, 0.16, -0.201015]],
                     [-0.391128, [3, -0.16, 0.162972], [3, 0.173333, -0.176553]],
                     [-0.796104, [3, -0.173333, 0.151293], [3, 0.16, -0.139655]],
                     [-1.26397, [3, -0.16, 0.022656], [3, 0.173333, -0.024544]],
                     [-1.28852, [3, -0.173333, 0], [3, 0.16, 0]
                      ], [-1.28698, [3, -0.16, 0], [3, 0.173333, 0]],
                     [-1.28698, [3, -0.173333, 0], [3, 0.16, 0]
                      ], [-1.28545, [3, -0.16, 0], [3, 0.173333, 0]],
                     [-1.28545, [3, -0.173333, 0], [3, 0.16, 0]
                      ], [-1.28545, [3, -0.16, 0], [3, 0.173333, 0]],
                     [-1.28545, [3, -0.173333, 0], [3, 0.16, 0]], [-1.28545, [3, -0.16, 0], [3, 0, 0]]])

        names.append("RShoulderRoll")
        times.append(
            [0.52, 1.04, 1.52, 2.04, 2.52, 3.04, 3.52, 4.04, 4.52, 5.04, 5.52, 6.04, 6.52, 7.04, 7.52, 8.04, 8.52])
        keys.append([[0.171766, [3, -0.173333, 0], [3, 0.173333, 0]], [0.171766, [3, -0.173333, 0], [3, 0.16, 0]],
                     [0.171766, [3, -0.16, 0], [3, 0.173333, 0]
                      ], [0.177902, [3, -0.173333, 0], [3, 0.16, 0]],
                     [0.139552, [3, -0.16, 0.0105539], [3, 0.173333, -0.0114334]],
                     [0.11194, [3, -0.173333, 0.0109016], [3, 0.16, -0.0100631]],
                     [0.076658, [3, -0.16, 0.0228259], [3, 0.173333, -0.0247281]],
                     [-0.0307219, [3, -0.173333, 0.0239304], [3, 0.16, -0.0220896]],
                     [-0.0614018, [3, -0.16, 0], [3, 0.173333, 0]],
                     [-0.0598679, [3, -0.173333, -0.00153398], [3, 0.16, 0.00141599]],
                     [-0.044528, [3, -0.16, -0.00368156],
                         [3, 0.173333, 0.00398836]],
                     [-0.0368581, [3, -0.173333, 0], [3, 0.16, 0]],
                     [-0.0383921, [3, -0.16, 0.00153398],
                         [3, 0.173333, -0.00166182]],
                     [-0.0859461, [3, -0.173333, 0], [3, 0.16, 0]
                      ], [-0.0859461, [3, -0.16, 0], [3, 0.173333, 0]],
                     [-0.0567999, [3, -0.173333, 0], [3, 0.16, 0]], [-0.067538, [3, -0.16, 0], [3, 0, 0]]])

        names.append("RWristYaw")
        times.append(
            [0.52, 1.04, 1.52, 2.04, 2.52, 3.04, 3.52, 4.04, 4.52, 5.04, 5.52, 6.04, 6.52, 7.04, 7.52, 8.04, 8.52])
        keys.append([[-0.909704, [3, -0.173333, 0], [3, 0.173333, 0]], [-0.909704, [3, -0.173333, 0], [3, 0.16, 0]],
                     [-0.909704, [3, -0.16, 0], [3, 0.173333, 0]
                      ], [-0.909704, [3, -0.173333, 0], [3, 0.16, 0]],
                     [-0.604438, [3, -0.16, -0.0566401], [3, 0.173333, 0.0613601]],
                     [-0.543078, [3, -0.173333, -0.0297801], [3, 0.16, 0.0274893]],
                     [-0.43263, [3, -0.16, -0.026753], [3, 0.173333, 0.0289824]],
                     [-0.375872, [3, -0.173333, -0.0194102], [3, 0.16, 0.0179171]],
                     [-0.320648, [3, -0.16, 0], [3, 0.173333, 0]],
                     [-0.533874, [3, -0.173333, 0.0199418], [3, 0.16, -0.0184078]],
                     [-0.552282, [3, -0.16, 0], [3, 0.173333, 0]
                      ], [-0.552282, [3, -0.173333, 0], [3, 0.16, 0]],
                     [-0.552282, [3, -0.16, 0], [3, 0.173333, 0]
                      ], [-0.549214, [3, -0.173333, 0], [3, 0.16, 0]],
                     [-0.549214, [3, -0.16, 0], [3, 0.173333, 0]
                      ], [-0.550748, [3, -0.173333, 0], [3, 0.16, 0]],
                     [-0.549214, [3, -0.16, 0], [3, 0, 0]]])

        try:
            # TODO: use self.ip, self.host
            motion = ALProxy("ALMotion", self.ip, self.port)
            if (motion.robotIsWakeUp()):
                motion.rest()
            # motion.wakeUp()
            motion.setStiffnesses("Body", 1.0)
            motion.angleInterpolationBezier(names, times, keys)
            time.sleep(5)
            motion.rest()
        except BaseException, err:
            print err

if __name__ == "__main__":
    pass
