import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import os
import queue
import threading
import numpy as np
import tflite_runtime.interpreter as tflite

class SignLanguageApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.setup_model()
        self.setup_tts()
        
    def setup_ui(self):
        # Thiết lập giao diện người dùng
        self.root.title("Sign Language Recognition - Raspberry Pi")
        self.root.geometry("800x600")
        
        # Tạo các thành phần UI
        self.create_camera_display()
        self.create_control_panel()
        self.create_info_labels()
        
    def setup_model(self):
        # Tải mô hình TFLite
        self.interpreter = tflite.Interpreter(model_path='models/sign_language.tflite')
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
    def setup_tts(self):
        # Thiết lập text-to-speech
        self.tts_enabled = True
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)
        except:
            self.tts_enabled = False
            
    # ... (các phương thức khác giữ nguyên)