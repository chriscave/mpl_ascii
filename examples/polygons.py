import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon




if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--out", type=str, required=False)
    parser.add_argument("--ascii", action="store_true")

    args = parser.parse_args()
    out = args.out
    asci = args.ascii

    if asci:
        mpl.use("module://mpl_ascii")

# Create a figure with 2x2 subplots
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    # Define polygon vertices for different shapes
    triangle = np.array([[0.2, 0.2], [0.8, 0.2], [0.5, 0.8]])
    pentagon = np.array([[0.5, 0.2], [0.8, 0.4], [0.7, 0.7], [0.3, 0.7], [0.2, 0.4]])
    hexagon = np.array([[0.5, 0.2], [0.7, 0.3], [0.7, 0.6], [0.5, 0.7], [0.3, 0.6], [0.3, 0.3]])
    star = np.array([[0.5, 0.9], [0.4, 0.6], [0.1, 0.5], [0.4, 0.4], [0.5, 0.1],
                    [0.6, 0.4], [0.9, 0.5], [0.6, 0.6]])

    # Array of polygons and their properties
    polygons = [
        (triangle, 'cyan', 'Triangle', axes[0, 0]),
        (pentagon, 'lime', 'Pentagon', axes[0, 1]),
        (hexagon, 'yellow', 'Hexagon', axes[1, 0]),
        (star, 'magenta', 'Star', axes[1, 1])
    ]

    # Add polygons to subplots
    for poly_verts, color, title, ax in polygons:
        polygon = Polygon(poly_verts, closed=True, facecolor=color, alpha=0.5, edgecolor='black')
        ax.add_patch(polygon)
        ax.set_title(title)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.grid(True, linestyle='--', alpha=0.7)

    # Adjust layout to prevent overlap
    fig.tight_layout()

    # Display the plot
    plt.show()


    if out:
        fig.savefig(out)
