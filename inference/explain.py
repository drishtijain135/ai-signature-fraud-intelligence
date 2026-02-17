import os
import uuid
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

def generate_explainability(diff):
    # Ensure static folder exists
    os.makedirs("static", exist_ok=True)

    # Normalize diff for better visualization
    diff_normalized = (diff - np.min(diff)) / (np.max(diff) - np.min(diff) + 1e-8)

    # Unique filename (prevents overwrite)
    filename = f"explainability_{uuid.uuid4().hex}.png"
    filepath = os.path.join("static", filename)

    # Plot heatmap
    plt.figure(figsize=(4, 3))
    plt.imshow(diff_normalized[0].squeeze(), cmap="hot")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(filepath, bbox_inches="tight", pad_inches=0)
    plt.close()

    return filename


