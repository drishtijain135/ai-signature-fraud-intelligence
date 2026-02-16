import tensorflow as tf
from tensorflow.keras import layers, Model

IMG_HEIGHT = 155
IMG_WIDTH = 220


def build_base_network():
    """
    CNN feature extractor
    """

    inputs = tf.keras.Input(shape=(IMG_HEIGHT, IMG_WIDTH, 1))

    x = layers.Conv2D(32, (3, 3), activation="relu")(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D()(x)

    x = layers.Conv2D(64, (3, 3), activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D()(x)

    x = layers.Conv2D(128, (3, 3), activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D()(x)

    x = layers.Flatten()(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dropout(0.3)(x)

    outputs = layers.Dense(128)(x)

    return Model(inputs, outputs, name="FeatureExtractor")


def build_siamese_model():
    """
    Siamese Network using distance metric
    """

    base_network = build_base_network()

    input_a = tf.keras.Input(shape=(IMG_HEIGHT, IMG_WIDTH, 1))
    input_b = tf.keras.Input(shape=(IMG_HEIGHT, IMG_WIDTH, 1))

    embedding_a = base_network(input_a)
    embedding_b = base_network(input_b)

    # Euclidean distance
    distance = tf.keras.layers.Lambda(
        lambda tensors: tf.math.abs(tensors[0] - tensors[1])
    )([embedding_a, embedding_b])

    output = layers.Dense(1, activation="sigmoid")(distance)

    model = Model(inputs=[input_a, input_b], outputs=output)

    model.compile(
        loss="binary_crossentropy",
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
        metrics=["accuracy"]
    )

    return model
