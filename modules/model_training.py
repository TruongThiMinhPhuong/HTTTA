import os
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import cv2
import pickle

def load_data():
    data = []
    labels = []
    
    for folder in os.listdir("data"):
        if os.path.isdir(os.path.join("data", folder)):
            for img_file in os.listdir(os.path.join("data", folder)):
                if img_file.endswith('.jpg'):
                    img_path = os.path.join("data", folder, img_file)
                    img = cv2.imread(img_path)
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    img = cv2.resize(img, (64, 64))
                    data.append(img)
                    labels.append(folder)
    
    data = np.array(data, dtype="float32") / 255.0
    data = np.expand_dims(data, axis=-1)  # Thêm channel cho grayscale
    
    le = LabelEncoder()
    labels = le.fit_transform(labels)
    labels = to_categorical(labels, 26)
    
    return data, labels, le

def train_model():
    data, labels, le = load_data()
    
    (X_train, X_test, y_train, y_test) = train_test_split(
        data, labels, test_size=0.2, random_state=42)
    
    # Xây dựng mô hình đơn giản cho RPi
    model = Sequential([
        Conv2D(32, (3,3), activation='relu', input_shape=(64,64,1)),
        MaxPooling2D(2,2),
        Conv2D(64, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(26, activation='softmax')
    ])
    
    model.compile(loss='categorical_crossentropy',
                  optimizer=Adam(lr=0.001),
                  metrics=['accuracy'])
    
    # Huấn luyện với số epoch ít để chạy nhanh trên RPi
    model.fit(X_train, y_train, 
              validation_data=(X_test, y_test),
              batch_size=32,
              epochs=10,
              verbose=1)
    
    # Lưu mô hình và label encoder
    os.makedirs("models", exist_ok=True)
    model.save("models/sign_language_cnn.h5")
    with open("models/label_encoder.pkl", 'wb') as f:
        pickle.dump(le, f)
    
    print("Huấn luyện hoàn tất! Mô hình đã được lưu vào thư mục models/")