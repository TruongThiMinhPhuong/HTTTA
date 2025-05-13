import cv2
import numpy as np
import time
import tflite_runtime.interpreter as tflite

class RealTimePredictor:
    def __init__(self):
        self.interpreter = tflite.Interpreter(model_path='models/sign_language.tflite')
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.last_prediction = ''
        self.last_time = 0
        
    def preprocess(self, frame):
        roi = cv2.resize(frame, (48, 48))
        return roi.astype(np.float32) / 255.0
        
    def predict(self, frame):
        frame = cv2.flip(frame, 1)
        roi = frame[100:400, 150:450]
        
        # Tiền xử lý
        input_data = self.preprocess(roi)
        input_data = np.expand_dims(input_data, axis=0)
        
        # Dự đoán
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        output = self.interpreter.get_tensor(self.output_details[0]['index'])
        
        # Xử lý kết quả
        pred_idx = np.argmax(output)
        confidence = np.max(output)
        letter = chr(65 + pred_idx)  # A-Z
        
        # Giới hạn tốc độ dự đoán
        if time.time() - self.last_time > 1.0 and confidence > 0.8:
            self.last_prediction = letter
            self.last_time = time.time()
            
        # Vẽ kết quả
        cv2.rectangle(frame, (150, 100), (450, 400), (0, 255, 0), 2)
        cv2.putText(frame, f"Pred: {self.last_prediction}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return frame, self.last_prediction