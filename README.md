sign-language-voice-system-pi/
│
├── data/ (thư mục chứa dữ liệu ảnh)
│   ├── A/
│   ├── B/
│   └── ... (26 thư mục từ A-Z)
│
├── models/ (thư mục chứa mô hình)
│   ├── sign_language_cnn.h5
│   └── label_encoder.pkl
│
├── modules/
│   ├── data_collection.py
│   ├── model_training.py
│   ├── realtime_prediction.py
│   └── text_to_speech.py
│
├── app.py (giao diện chính)
├── requirements.txt
└── README.md

# Sign Language Recognition on Raspberry Pi

## Installation
1. Flash Raspberry Pi OS Lite to SD card
2. Enable SSH and WiFi
3. Connect to Pi via SSH and run:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-opencv libatlas-base-dev
pip3 install -r requirements.txt
Yêu Cầu Phần Cứng:
Usage
Collect data:

bash
python3 app.py --mode collect --letter A
Train model:

bash
python3 app.py --mode train
Run real-time recognition:


python3 app.py --mode predict 
```
Raspberry Pi 4 (Model B với 2GB/4GB/8GB RAM)

Thẻ nhớ microSD 32GB trở lên

Webcam USB (tương thích với Raspberry Pi)

Loa hoặc tai nghe có jack 3.5mm

Màn hình, bàn phím, chuột (cho thiết lập ban đầu)

# Cập nhật hệ thống
sudo apt update && sudo apt upgrade -y

# Cài đặt các gói cần thiết
sudo apt install -y python3-pip python3-opencv libatlas-base-dev libjasper-dev libqtgui4 libqt4-test

# Cài đặt các thư viện Python
pip3 install tensorflow-2.10.0-cp39-none-linux_aarch64.whl  # Tải file wheel phù hợp
pip3 install opencv-python==4.5.3.56 numpy==1.19.4 pyttsx3==2.90 Pillow==9.0.1 scikit-learn==0.24.2

# Cài đặt thư viện âm thanh
sudo apt install -y espeak pulseaudio

Hướng Dẫn Chạy Ứng Dụng
Sao chép dự án lên Raspberry Pi:

scp -r sign-language-system pi@<your-pi-ip>:~/
Cấp quyền cho webcam:


sudo usermod -a -G video pi

Khởi động ứng dụng:


cd ~/sign-language-system
python3 app.py

Lỗi không nhận diện được webcam:

sudo apt install v4l-utils
v4l2-ctl --list-devices

Lỗi thiếu thư viện OpenCV:

sudo apt install libatlas-base-dev libhdf5-dev libhdf5-serial-dev

Hiệu suất thấp:

Giảm kích thước ảnh đầu vào (từ 64x64 xuống 48x48)

Sử dụng mô hình nhỏ hơn

Âm thanh không hoạt động:

sudo raspi-config  # Chọn Audio > Headphone