import subprocess
import threading

class TextToSpeech:
    def __init__(self):
        self.available = self.check_espeak()
        
    def check_espeak(self):
        try:
            subprocess.run(['espeak', '--version'], check=True)
            return True
        except:
            return False
            
    def speak(self, text):
        if not self.available:
            return
            
        def _speak():
            subprocess.run(['espeak', '-ven+f3', text])
            
        thread = threading.Thread(target=_speak)
        thread.start()