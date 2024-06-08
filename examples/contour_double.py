import argparse
import matplotlib as mpl

mpl.use("module://mpl_ascii")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--out", type=str)

    args = parser.parse_args()
    out = args.out

    import matplotlib.pyplot as plt
    import numpy as np

    # Create a grid of x and y values
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)

    # Define two functions to generate contour data
    Z1 = np.sin(np.sqrt(X**2 + Y**2))
    Z2 = np.cos(np.sqrt(X**2 + Y**2))

    # Create a figure and axis object
    fig, ax = plt.subplots()

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

    # Show the plot

    if out:
        fig.savefig(out)

    plt.show()
