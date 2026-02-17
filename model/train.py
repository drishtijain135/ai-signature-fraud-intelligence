import os
import random
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf

from preprocessing.preprocess import preprocess_image
from model.siamese_model import build_siamese_model

DATA_DIR = "data"
GENUINE_DIR = os.path.join(DATA_DIR, "genuine")
FORGED_DIR = os.path.join(DATA_DIR, "forged")

VALID_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp")


def load_image_paths():
    genuine_images = [
        os.path.join(GENUINE_DIR, f)
        for f in os.listdir(GENUINE_DIR)
        if f.lower().endswith(VALID_EXTENSIONS)
    ]

    forged_images = [
        os.path.join(FORGED_DIR, f)
        for f in os.listdir(FORGED_DIR)
        if f.lower().endswith(VALID_EXTENSIONS)
    ]

    return genuine_images, forged_images


def create_pairs(genuine, forged):
    pairs = []
    labels = []

    random.shuffle(genuine)
    random.shuffle(forged)

    # Create balanced positive and negative pairs
    num_pairs = min(len(genuine), len(forged))

    # Positive pairs (random genuine-genuine)
    for _ in range(num_pairs):
        img1 = random.choice(genuine)
        img2 = random.choice(genuine)
        pairs.append([img1, img2])
        labels.append(1)

    # Negative pairs (genuine-forged)
    for _ in range(num_pairs):
        img1 = random.choice(genuine)
        img2 = random.choice(forged)
        pairs.append([img1, img2])
        labels.append(0)

    return pairs, labels


def preprocess_pairs(pairs):
    img1 = []
    img2 = []

    for pair in pairs:
        img1.append(preprocess_image(pair[0]))
        img2.append(preprocess_image(pair[1]))

    return np.array(img1), np.array(img2)


def main():

    print("Loading dataset...")
    genuine, forged = load_image_paths()

    print(f"Genuine images: {len(genuine)}")
    print(f"Forged images: {len(forged)}")

    print("Creating pairs...")
    pairs, labels = create_pairs(genuine, forged)

    labels = np.array(labels)

    print("Preprocessing images...")
    img1, img2 = preprocess_pairs(pairs)

    X_train_1, X_val_1, X_train_2, X_val_2, y_train, y_val = train_test_split(
        img1, img2, labels, test_size=0.2, random_state=42, stratify=labels
    )

    print("Building model...")
    model = build_siamese_model()

    # Callbacks
    early_stop = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True
    )

    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=3,
        verbose=1
    )

    print("Training model...")
    model.fit(
        [X_train_1, X_train_2],
        y_train,
        validation_data=([X_val_1, X_val_2], y_val),
        epochs=30,
        batch_size=16,
        callbacks=[early_stop, reduce_lr]
    )

    print("Saving model...")
    model.save("signature_model.h5")

    print("Training complete!")


if __name__ == "__main__":
    main()
