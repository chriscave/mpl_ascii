import argparse
import matplotlib as mpl
import numpy as np


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--out", type=str, required=False)
    parser.add_argument("--ascii", action="store_true")

    args = parser.parse_args()
    out = args.out
    asci = args.ascii

    if asci:
        mpl.use("module://mpl_ascii")

    # data from https://allisonhorst.github.io/palmerpenguins/

    import matplotlib.pyplot as plt

    delta = 0.025
    x = np.arange(-3.0, 3.0, delta)
    y = np.arange(-2.0, 2.0, delta)
    X, Y = np.meshgrid(x, y)
    Z1 = np.exp(-X**2 - Y**2)
    Z2 = np.exp(-(X - 1)**2 - (Y - 1)**2)
    Z = (Z1 - Z2) * 2

    fig, axes = plt.subplots(1,2, figsize=(10,4))
    ax = axes[0]
    CS = ax.contour(X, Y, Z)
    ax.clabel(CS, inline=True, fontsize=10)
    ax.set_title('Simplest default with labels')


    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)

    # Define two functions to generate contour data
    Z1 = np.sin(np.sqrt(X**2 + Y**2))
    Z2 = np.cos(np.sqrt(X**2 + Y**2))

    # Create a figure and axis object

    ax = axes[1]

    # Create the contour plots
    contour1 = ax.contour(X, Y, Z1, colors='blue')
    contour2 = ax.contour(X, Y, Z2, colors='red')

    # Add labels and title
    ax.set_title('Contour Plots of Two Functions')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')

    # Add a legend
    h1,_ = contour1.legend_elements()
    h2,_ = contour2.legend_elements()
    ax.legend([h1[0], h2[0]], ['sin(sqrt(x^2 + y^2))', 'cos(sqrt(x^2 + y^2))'])


    fig.tight_layout()

    plt.show()

    if out:
        fig.savefig(out)
