import matplotlib.pyplot as plt
import numpy as np

def generate_heatmap(img1, img2):
    diff = np.abs(img1 - img2)

    plt.imshow(diff[0].squeeze(), cmap="hot")
    plt.axis("off")
    plt.savefig("heatmap.png", bbox_inches="tight")
    plt.close()
