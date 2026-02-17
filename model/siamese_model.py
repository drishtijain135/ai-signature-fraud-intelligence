import tensorflow as tf
from tensorflow.keras import layers, Model

IMG_HEIGHT = 155
IMG_WIDTH = 220


def build_base_network():
    """
    Improved CNN feature extractor
    """

    inputs = tf.keras.Input(shape=(IMG_HEIGHT, IMG_WIDTH, 1))

    # Block 1
    x = layers.Conv2D(32, (3, 3), padding="same", activation="relu")(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D()(x)

    # Block 2
    x = layers.Conv2D(64, (3, 3), padding="same", activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D()(x)

    # Block 3
    x = layers.Conv2D(128, (3, 3), padding="same", activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D()(x)

    # Block 4 (NEW – deeper features)
    x = layers.Conv2D(256, (3, 3), padding="same", activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D()(x)

    x = layers.Flatten()(x)

    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dropout(0.5)(x)

    # Embedding layer
    x = layers.Dense(128)(x)

    # Normalize embeddings (VERY IMPORTANT for Siamese)
    outputs = layers.Lambda(lambda t: tf.math.l2_normalize(t, axis=1))(x)

    return Model(inputs, outputs, name="FeatureExtractor")


def euclidean_distance(vectors):
    x, y = vectors
    return tf.sqrt(tf.reduce_sum(tf.square(x - y), axis=1, keepdims=True))


def build_siamese_model():
    """
    Improved Siamese Network
    """

    base_network = build_base_network()

    input_a = tf.keras.Input(shape=(IMG_HEIGHT, IMG_WIDTH, 1))
    input_b = tf.keras.Input(shape=(IMG_HEIGHT, IMG_WIDTH, 1))

    embedding_a = base_network(input_a)
    embedding_b = base_network(input_b)

    # TRUE Euclidean distance
    distance = layers.Lambda(euclidean_distance)([embedding_a, embedding_b])

    output = layers.Dense(1, activation="sigmoid")(distance)

    model = Model(inputs=[input_a, input_b], outputs=output)

    model.compile(
        loss="binary_crossentropy",
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
        metrics=["accuracy"]
    )

    return model
