import cv2
import os
import time

def collect(letter):
    save_dir = os.path.join("data", letter.upper())
    os.makedirs(save_dir, exist_ok=True)
    
    # Đếm số file ảnh đã có
    existing_files = len([name for name in os.listdir(save_dir) if name.endswith('.jpg')])
    count = existing_files
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    if not cap.isOpened():
        print("Không thể mở camera.")
        return

    print(f"Bắt đầu thu thập dữ liệu cho chữ: {letter}")
    
    while count < 100 + existing_files:
        ret, frame = cap.read()
        if not ret:
            print("Không thể đọc khung hình.")
            break

        frame = cv2.flip(frame, 1)
        roi = frame[100:300, 100:300]  # Vùng ROI nhỏ hơn cho Raspberry Pi
        
        # Hiển thị hướng dẫn
        cv2.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 2)
        cv2.putText(frame, f"Dang thu: {letter}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.putText(frame, f"So luong: {count}/100", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.putText(frame, "Nhan 'q' de thoat", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv2.imshow("Thu thap du lieu", frame)
        
        # Tự động lưu ảnh mỗi 0.3 giây
        img_path = os.path.join(save_dir, f"{count}.jpg")
        cv2.imwrite(img_path, roi)
        count += 1
        time.sleep(0.3)  # Giảm tốc độ thu thập cho RPi

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Đã lưu {count-existing_files} ảnh mới vào {save_dir}")