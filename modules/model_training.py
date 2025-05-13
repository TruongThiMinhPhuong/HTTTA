import tensorflow as tf
import numpy as np
import os
import cv2
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

class ModelTrainer:
    def __init__(self, img_size=48):
        self.img_size = img_size
        
    def load_data(self):
        X, y = [], []
        for label in os.listdir('data'):
            for img_file in os.listdir(f'data/{label}'):
                img = cv2.imread(f'data/{label}/{img_file}')
                img = cv2.resize(img, (self.img_size, self.img_size))
                X.append(img)
                y.append(label)
        return np.array(X), np.array(y)
        
    def train(self):
        X, y = self.load_data()
        
        # Tiền xử lý dữ liệu
        X = X / 255.0
        le = LabelEncoder()
        y = le.fit_transform(y)
        
        # Chia tập train/test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        # Xây dựng mô hình đơn giản cho Pi
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(16, (3,3), activation='relu', input_shape=(self.img_size, self.img_size, 3)),
            tf.keras.layers.MaxPooling2D(2,2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(len(np.unique(y)), activation='softmax')
        ])
        
        model.compile(optimizer='adam',
                    loss='sparse_categorical_crossentropy',
                    metrics=['accuracy'])
        
        model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))
        
        # Chuyển đổi sang TFLite
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        tflite_model = converter.convert()
        
        os.makedirs('models', exist_ok=True)
        with open('models/sign_language.tflite', 'wb') as f:
            f.write(tflite_model)