import speech_recognition as sr

class STT:
    def __init__(self):
        self._r = sr.Recognizer()
        self._mic = sr.Microphone()

    def recognize(self):    
        with self._mic as source:
            audio = self._r.listen(source)
        return self._r.recognize_google(audio)
