import cv2
import numpy as np
from tensorflow.keras.models import load_model
import pickle

model = None
le = None

def load_models():
    global model, le
    try:
        model = load_model("models/sign_language_cnn.h5")
        with open("models/label_encoder.pkl", 'rb') as f:
            le = pickle.load(f)
    except:
        print("Warning: Models not loaded! Please train first.")
        return False
    return True

def predict_from_frame(frame):
    if model is None or le is None:
        if not load_models():
            return None
    
    roi = frame[100:300, 100:300]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (64, 64))
    normalized = resized.astype("float32") / 255.0
    reshaped = np.expand_dims(normalized, axis=-1)
    reshaped = np.expand_dims(reshaped, axis=0)
    
    preds = model.predict(reshaped)
    pred_label = np.argmax(preds, axis=1)
    letter = le.inverse_transform(pred_label)[0]
    
    if np.max(preds) > 0.8:
        return letter
    return None