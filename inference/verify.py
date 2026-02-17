import cv2
import numpy as np

def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (220, 155))
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = img / 255.0
    img = img.reshape(1, 155, 220, 1)
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
from inference.explain import generate_explainability

def verify_signature(file1, file2):
    img1 = preprocess_image(file1)
    img2 = preprocess_image(file2)

    similarity = predict_similarity(img1, img2)

    risk_data = calculate_risk(similarity)
    generate_explainability(img1)

    result = "Genuine" if similarity > 0.5 else "Forged"

    return {
        "result": result,
        "similarity": round(similarity, 2),
        **risk_data
    }
