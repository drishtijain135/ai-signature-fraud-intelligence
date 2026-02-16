import tensorflow as tf
from tensorflow.keras import layers, Model

IMG_WIDTH = 220
IMG_HEIGHT = 155

def build_base_network():
    input = layers.Input((IMG_HEIGHT, IMG_WIDTH, 1))

    x = layers.Conv2D(32, (3,3), activation='relu')(input)
    x = layers.MaxPooling2D()(x)

    x = layers.Conv2D(64, (3,3), activation='relu')(x)
    x = layers.MaxPooling2D()(x)

    x = layers.Conv2D(128, (3,3), activation='relu')(x)
    x = layers.MaxPooling2D()(x)

    x = layers.Flatten()(x)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dropout(0.4)(x)

    return Model(input, x)

def build_siamese_model():
    base_network = build_base_network()

    input_a = layers.Input((IMG_HEIGHT, IMG_WIDTH, 1))
    input_b = layers.Input((IMG_HEIGHT, IMG_WIDTH, 1))

    processed_a = base_network(input_a)
    processed_b = base_network(input_b)

    merged = layers.Concatenate()([processed_a, processed_b])
    output = layers.Dense(1, activation='sigmoid')(merged)

    model = Model([input_a, input_b], output)
    return model
