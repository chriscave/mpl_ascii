import argparse
import matplotlib as mpl

mpl.use("module://mpl_ascii")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--out", type=str)

    args = parser.parse_args()
    out = args.out

    import numpy as np
    import matplotlib.pyplot as plt

    # Generating some data
    np.random.seed(19680802)

    x = np.random.rand(100) * 100  # Random values for x-axis
    y = np.random.rand(100) * 100  # Random values for y-axis
    values = np.random.randint(low=0, high=16, size=100)   # Values to determine the color of each point
    # values = np.random.rand(100)   # Values to determine the color of each point
    # Create the plot
    fig, ax = plt.subplots()

    # Create a scatter plot
    scatter = ax.scatter(x, y, c=values, cmap='viridis')

    # Create a colorbar
    colorbar = plt.colorbar(scatter)
    colorbar.set_label('Intensity')

    # Setting labels and title
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_title('Scatter Plot with Color Bar')

    if out:
        fig.savefig(out)

    plt.show()
