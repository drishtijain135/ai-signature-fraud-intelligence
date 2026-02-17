import cv2
import numpy as np
from tensorflow.keras.models import load_model


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
    print("✅ Trained model loaded successfully.")
except Exception as e:
    print("⚠️ Trained model not found. Using dummy model for testing.")
    print("Error:", e)


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
from inference.logger import log_result


def verify_signature(file1, file2):
    import time
    start_time = time.time()

    img1 = preprocess_image(file1)
    img2 = preprocess_image(file2)

    similarity = predict_similarity(img1, img2)

    risk_data = calculate_risk(similarity)

    diff = np.abs(img1 - img2)
    explainability_file = generate_explainability(diff)

    result = "Genuine" if similarity > 0.5 else "Forged"

    log_result({
        "result": result,
        "similarity": round(float(similarity), 2),
        **risk_data
    })

    execution_time = round(time.time() - start_time, 3)

    return {
        "status": "success",
        "prediction": {
            "result": result,
            "similarity": round(float(similarity), 2)
        },
        "risk_analysis": {
            "risk_score": risk_data["risk_score"],
            "risk_level": risk_data["risk_level"],
            "fraud_probability": risk_data["fraud_probability"],
            "behavioral_deviation_index": risk_data["behavioral_deviation_index"]
        },
        "explainability": {
            "heatmap_url": f"http://127.0.0.1:5000/static/{explainability_file}"
        },
        "metadata": {
            "execution_time_seconds": execution_time
        }
    }


