import speech_recognition as sr

class STT:
    def __init__(self):
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()

    def recognize(self):    
        with self.mic as source:
            audio = self.r.listen(source)
        text = self.r.recognize_google(audio)
        return text
