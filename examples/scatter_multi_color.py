import argparse
import matplotlib as mpl
import mpl_ascii

mpl_ascii.AXES_WIDTH=100
mpl_ascii.AXES_HEIGHT=40

mpl.use("module://mpl_ascii")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--out", type=str)

    args = parser.parse_args()
    out = args.out
    import matplotlib.pyplot as plt
    import numpy as np

    # Generate some random data
    np.random.seed(0)
    x = np.random.rand(40)
    y = np.random.rand(40)
    colors = np.random.choice(['red', 'green', 'blue', 'yellow'], size=40)
    color_labels = ['Red', 'Green', 'Blue', 'Yellow']  # Labels corresponding to colors

    # Create a scatter plot
    fig, ax = plt.subplots()
    for color, label in zip(['red', 'green', 'blue', 'yellow'], color_labels):
        # Plot each color as a separate scatter plot to enable legend tracking
        idx = np.where(colors == color)
        ax.scatter(x[idx], y[idx], color=color, label=label)

    # Set title and labels
    ax.set_title('Scatter Plot with 4 Different Colors')
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')

    # Add a legend
    ax.legend(title='Point Colors')


    if out:
        fig.savefig(out)

    plt.show()