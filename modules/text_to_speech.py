import os
import subprocess
from typing import Optional

class TextToSpeech:
    def __init__(self):
        self.engine = None
        self.setup_engine()

    def setup_engine(self):
        """Khởi tạo engine TTS với các fallback phù hợp cho Raspberry Pi"""
        try:
            import pyttsx3
            self.engine_type = 'pyttsx3'
            self.engine = pyttsx3.init()
            
            # Cấu hình cho Raspberry Pi
            self.engine.setProperty('rate', 150)  # Tốc độ đọc
            voices = self.engine.getProperty('voices')
            
            # Ưu tiên giọng nữ nếu có
            if len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)
                
        except ImportError:
            self.engine_type = 'espeak'
            print("pyttsx3 không khả dụng, sử dụng espeak làm fallback")

    def speak(self, text: str, lang: Optional[str] = 'vi') -> bool:
        """
        Phát âm văn bản
        :param text: Văn bản cần phát âm
        :param lang: Ngôn ngữ (vi/en)
        :return: True nếu thành công
        """
        if not text:
            return False

        try:
            if self.engine_type == 'pyttsx3' and self.engine:
                self.engine.say(text)
                self.engine.runAndWait()
                return True
            else:
                # Fallback sử dụng espeak
                lang_option = '-v' + ('vi' if lang == 'vi' else 'en')
                cmd = ['espeak', lang_option, text]
                subprocess.run(cmd, check=True)
                return True
        except Exception as e:
            print(f"Lỗi phát âm: {str(e)}")
            return False

# Phiên bản đơn giản để tương thích ngược
def speak(text: str):
    tts = TextToSpeech()
    return tts.speak(text)

if __name__ == "__main__":
    # Test các chức năng
    tts = TextToSpeech()
    tts.speak("Xin chào, đây là hệ thống chuyển ngôn ngữ ký hiệu thành giọng nói")
    tts.speak("Hello, this is sign language to speech system", lang='en')