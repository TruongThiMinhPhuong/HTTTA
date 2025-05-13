import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import os
from modules import data_collection, model_training, realtime_prediction, text_to_speech

class SignLanguageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HỆ THỐNG NHẬN DIỆN NGÔN NGỮ KÝ HIỆU")
        self.root.geometry("1000x600")
        self.cap = None
        self.running = False

        # ========== KHUNG ĐIỀU KHIỂN ==========
        left_frame = tk.Frame(root, width=200, bg="#f0f0f0")
        left_frame.pack(side="left", fill="y")

        btn_thu_thap = tk.Button(left_frame, text="THU THẬP DỮ LIỆU", command=self.thu_thap)
        btn_thu_thap.pack(pady=5, fill="x")

        btn_huan_luyen = tk.Button(left_frame, text="HUẤN LUYỆN MÔ HÌNH", command=self.huan_luyen)
        btn_huan_luyen.pack(pady=5, fill="x")

        btn_nhan_dien = tk.Button(left_frame, text="NHẬN DIỆN THỜI GIAN THỰC", command=self.bat_camera)
        btn_nhan_dien.pack(pady=5, fill="x")

        btn_phat_am = tk.Button(left_frame, text="PHÁT ÂM CÂU", command=self.phat_am)
        btn_phat_am.pack(pady=5, fill="x")

        btn_xoa = tk.Button(left_frame, text="XÓA CÂU", command=self.xoa_cau)
        btn_xoa.pack(pady=5, fill="x")

        btn_dung = tk.Button(left_frame, text="DỪNG CAMERA", command=self.dung_camera)
        btn_dung.pack(pady=5, fill="x")

        btn_thoat = tk.Button(left_frame, text="THOÁT", command=root.quit)
        btn_thoat.pack(pady=5, fill="x")

        self.letter_var = tk.StringVar()
        self.letter_combo = ttk.Combobox(left_frame, textvariable=self.letter_var, values=[chr(i) for i in range(65, 91)])
        self.letter_combo.pack(pady=5, fill="x")
        self.letter_combo.set("A")

        self.status_label = tk.Label(left_frame, text="Đang thu thập dữ liệu cho chữ: A", bg="#f0f0f0")
        self.status_label.pack(pady=5)

        # ========== KHUNG HIỂN THỊ CAMERA ==========
        right_frame = tk.Frame(root, bg="white")
        right_frame.pack(side="right", expand=True, fill="both")

        self.video_label = tk.Label(right_frame, bg="black")
        self.video_label.pack(expand=True, fill="both")

        # ========== KẾT QUẢ ==========
        result_frame = tk.Frame(right_frame, bg="#ffffff")
        result_frame.pack(fill="x", pady=10)

        tk.Label(result_frame, text="KẾT QUẢ:", font=("Arial", 12, "bold")).pack(side="left")
        self.cau_label = tk.Label(result_frame, text="CÂU: ", font=("Arial", 12, "bold"))
        self.cau_label.pack(side="left")

        self.predicted_text = ""

    def thu_thap(self):
        chu = self.letter_var.get()
        self.status_label.config(text=f"Đang thu thập dữ liệu cho chữ: {chu}")
        data_collection.collect(chu)

    def huan_luyen(self):
        model_training.train_model()
        self.status_label.config(text="Huấn luyện mô hình xong!")

    def phat_am(self):
        text_to_speech.speak(self.predicted_text)

    def xoa_cau(self):
        self.predicted_text = ""
        self.cau_label.config(text="CÂU: ")

    def bat_camera(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                self.status_label.config(text="Không mở được camera.")
                return
            self.running = True
            self.update_frame()

    def update_frame(self):
        if self.running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Gọi mô-đun nhận diện ký hiệu thời gian thực
                char = realtime_prediction.predict_from_frame(frame)
                if char:
                    self.predicted_text += char
                    self.cau_label.config(text=f"CÂU: {self.predicted_text}")

                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.config(image=imgtk)
            self.video_label.after(10, self.update_frame)

    def dung_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.video_label.config(image='', bg='black')

if __name__ == "__main__":
    root = tk.Tk()
    app = SignLanguageApp(root)
    root.mainloop()
