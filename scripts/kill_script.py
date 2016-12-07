from naoqi import ALProxy

if __name__ == "__main__":
    proxy = ALProxy("ALVideoRecorder", "localhost", 9559)
    proxy.stopRecording()
