import cv2
import numpy as np

IMG_WIDTH = 220
IMG_HEIGHT = 155

def preprocess_image(image_path):
    """
    Preprocess a signature image for Siamese network.

    Steps:
    1. Read grayscale
    2. Resize
    3. Otsu Threshold (binarization)
    4. Gaussian blur
    5. Normalize
    6. Add channel dimension
    """

    # 1️⃣ Read image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError(f"Could not load image: {image_path}")

    # 2️⃣ Resize
    img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))

    # 3️⃣ Otsu Thresholding (enhances signature strokes)
    _, img = cv2.threshold(
        img,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # 4️⃣ Light Gaussian blur (smooth edges slightly)
    img = cv2.GaussianBlur(img, (3, 3), 0)

    # 5️⃣ Normalize pixel values to [0,1]
    img = img.astype("float32") / 255.0

    # 6️⃣ Add channel dimension (H, W, 1)
    img = np.expand_dims(img, axis=-1)

    return img
