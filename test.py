from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "127.0.0.1", 49777)
tts.setLanguage("English")

tts.say("Hello!")
