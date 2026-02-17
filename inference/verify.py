import cv2
import numpy as np
from keras.models import load_model

def preprocess_image(image_bytes):
    image = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (220, 155))
    img = img / 255.0
    img = np.expand_dims(img, axis=(0, -1))
    return img
MODEL_PATH = "model/saved_model.h5"
#model = load_model(MODEL_PATH)
try:
    model = load_model(MODEL_PATH)
except:
    print("⚠️ Trained model not found. Using dummy model for testing.")

    class DummyModel:
        def predict(self, inputs):
            import numpy as np
            return np.array([[0.3]])  # simulate forged case

    model = DummyModel()



def predict_similarity(img1, img2):
    prediction = model.predict([img1, img2])[0][0]
    return prediction

from inference.risk import calculate_risk
from inference.explain import generate_heatmap

def verify_signature(file1, file2):
    img1 = preprocess_image(file1)
    img2 = preprocess_image(file2)

    similarity = predict_similarity(img1, img2)

    risk_data = calculate_risk(similarity)
    generate_heatmap(img1, img2)

    result = "Genuine" if similarity > 0.5 else "Forged"

    return {
        "result": result,
        "similarity": round(similarity, 2),
        **risk_data
    }
