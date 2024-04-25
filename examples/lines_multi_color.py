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

    # Set up the figure and axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create an array of x values
    x = np.linspace(-2 * np.pi, 2 * np.pi, 400)

    # Generate different continuous functions
    y1 = -x**2 - 4*x - 1
    y2 = np.tan(x)
    y3 = 8*np.exp(-x**2)  # Gaussian
    y4 = x**3 - 6*x**2 + 9*x  # Cubic polynomial



    # Plot the functions
    ax.plot(x, y1, label='-x**2 - 4x - 1')
    ax.plot(x, y2, label='tan(x)', clip_on=True)
    ax.plot(x, y3, label='8exp(-x^2)')
    ax.plot(x, y4, label='x^3 - 6x^2 + 9x')

    # Set labels, title, and legend
    ax.set_title('Plot of Continuous Functions')
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_ylim(-10, 10)  # Limit y-axis to avoid extreme values from tan(x)
    ax.legend()

    # Add grid
    ax.grid(True)

    # Show the plot

    if out:
        fig.savefig(out)

    plt.show()