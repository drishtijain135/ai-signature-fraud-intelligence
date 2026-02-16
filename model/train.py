import os
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import Adam

from preprocessing.preprocess import preprocess_image
from model.siamese_model import build_siamese_model

GENUINE_PATH = "data/genuine"
FORGED_PATH = "data/forged"

def load_images(folder):
    images = []
    for file in os.listdir(folder):
        images.append(preprocess_image(os.path.join(folder, file)))
    return images

def create_pairs(genuine, forged):
    pairs = []
    labels = []

    # Genuine vs Genuine (label = 1)
    for i in range(len(genuine)-1):
        pairs.append([genuine[i], genuine[i+1]])
        labels.append(1)

    # Genuine vs Forged (label = 0)
    for i in range(min(len(genuine), len(forged))):
        pairs.append([genuine[i], forged[i]])
        labels.append(0)

    return np.array(pairs), np.array(labels)

def main():
    genuine = load_images(GENUINE_PATH)
    forged = load_images(FORGED_PATH)

    pairs, labels = create_pairs(genuine, forged)

    X_train, X_test, y_train, y_test = train_test_split(
        pairs, labels, test_size=0.2, random_state=42
    )

    model = build_siamese_model()
    model.compile(
        loss='binary_crossentropy',
        optimizer=Adam(0.001),
        metrics=['accuracy']
    )

    model.fit(
        [X_train[:,0], X_train[:,1]],
        y_train,
        validation_data=([X_test[:,0], X_test[:,1]], y_test),
        batch_size=8,
        epochs=15
    )

    model.save("model/signature_model.h5")
    print("Model trained and saved successfully.")

if __name__ == "__main__":
    main()
