from naoqi import ALProxy

tts = ALProxy("ALTextToSpeech", "192.168.1.44", 9559)
motion = ALProxy("ALMotion", "192.168.1.44", 9559)
if motion.robotIsWakeUp():
    motion.rest()
else:
    motion.wakeUp()
    tts.say("Bonjour Roman.")
