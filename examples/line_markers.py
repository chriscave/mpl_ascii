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

    # Sample data
    x = np.linspace(0, 10, 50)
    y = np.sin(x)

    # Create a figure and a set of subplots
    fig, axs = plt.subplots(3, 2, figsize=(12, 18))

    # Basic Line Plot using fmt
    axs[0, 0].plot(x, y, 'b1')  # 'b-' is blue solid line
    axs[0, 0].set_title('Basic Line Plot')

    # Plot with Markers using fmt
    axs[0, 1].plot(x, y, 'r^')  # 'ro' is red circles
    axs[0, 1].set_title('Plot with Markers')

    # Dashed Line Plot using fmt
    axs[1, 0].plot(x, y, 'g--s')  # 'g--' is green dashed line
    axs[1, 0].set_title('Dashed Line Plot')

    # Customized Plot using fmt
    axs[1, 1].plot(x, y, 'c-.^')  # 'c-.^' is cyan dash-dot line with triangle up markers
    axs[1, 1].set_title('Customized Plot')

    # Multiple Lines in One Plot using fmt
    axs[2, 0].plot(x, y, 'r-<', label='sin(x)')  # 'k-' is black solid line
    axs[2, 0].plot(x, np.cos(x), 'b:>', label='cos(x)')  # 'm:s' is magenta dotted line with square markers
    axs[2, 0].set_title('Multiple Lines in One Plot')
    axs[2, 0].legend()

    # Remove empty subplot for cleaner appearance
    fig.delaxes(axs[2, 1])

    # Adjust layout
    plt.tight_layout()

    if out:
        fig.savefig(out)

    plt.show()
