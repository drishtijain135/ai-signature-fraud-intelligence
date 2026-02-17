import os
import uuid
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

STATIC_FOLDER = "static"
MAX_IMAGES = 10  # keep only last 10 images

def cleanup_old_images():
    files = sorted(
        [f for f in os.listdir(STATIC_FOLDER) if f.startswith("explainability_")],
        key=lambda x: os.path.getmtime(os.path.join(STATIC_FOLDER, x))
    )

    # Remove oldest files if limit exceeded
    while len(files) >= MAX_IMAGES:
        oldest = files.pop(0)
        os.remove(os.path.join(STATIC_FOLDER, oldest))


def generate_explainability(diff):

    os.makedirs(STATIC_FOLDER, exist_ok=True)

    # 🧹 Clean old images first
    cleanup_old_images()

    # Normalize diff
    diff_normalized = (diff - np.min(diff)) / (np.max(diff) - np.min(diff) + 1e-8)

    filename = f"explainability_{uuid.uuid4().hex}.png"
    filepath = os.path.join(STATIC_FOLDER, filename)

    plt.figure(figsize=(4, 3))
    plt.imshow(diff_normalized[0].squeeze(), cmap="hot")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(filepath, bbox_inches="tight", pad_inches=0)
    plt.close()

    return filename
