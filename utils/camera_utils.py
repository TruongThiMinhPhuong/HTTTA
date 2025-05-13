import cv2
import time

class PiCamera:
    def __init__(self, resolution=(640, 480), framerate=30):
        self.resolution = resolution
        self.framerate = framerate
        self.camera = None
        
    def __enter__(self):
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        self.camera.set(cv2.CAP_PROP_FPS, self.framerate)
        time.sleep(2)  # Thời gian khởi động camera
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.camera is not None:
            self.camera.release()
    
    def get_frame(self):
        if self.camera is None:
            return None
        
        ret, frame = self.camera.read()
        if not ret:
            return None
        
        # Giảm kích thước frame để tăng tốc độ xử lý
        frame = cv2.resize(frame, (320, 240))
        return frame