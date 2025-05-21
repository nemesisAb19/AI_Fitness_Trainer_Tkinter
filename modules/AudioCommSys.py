import pyttsx3
import speech_recognition as sr


class AudioFeedbackSystem:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.configure_engine()

    def configure_engine(self):
        self.engine.setProperty('rate', 175)
        self.engine.setProperty('volume', 1.0)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, prompt="Listening..."):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        print(prompt)
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return ""
        except sr.RequestError:
            print("Network error.")
            return ""

# def main():  
#     text_to_speech("Testing, Testing, Testing")

# if __name__ == "__main__":
#     main()
