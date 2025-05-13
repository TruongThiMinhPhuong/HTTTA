import os
import cv2
import time

class DataCollector:
    def __init__(self, letter='A', dataset_size=300):
        self.letter = letter
        self.dataset_size = dataset_size
        self.count = 0
        self.data_dir = f'data/{letter}'
        os.makedirs(self.data_dir, exist_ok=True)
        
    def capture_frame(self, frame):
        # Lật frame và vẽ hướng dẫn
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, f"Collecting: {self.letter}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Chụp và lưu ảnh
        if self.count < self.dataset_size:
            roi = frame[100:400, 150:450]
            timestamp = int(time.time() * 1000)
            cv2.imwrite(f"{self.data_dir}/{timestamp}.jpg", roi)
            self.count += 1
            
        return frame, self.count