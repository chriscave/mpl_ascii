import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
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


    x = np.arange(0.0, 2, 0.01)
    y1 = np.sin(2 * np.pi * x)
    y2 = 0.8 * np.sin(4 * np.pi * x)

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(8, 8))

    ax1.fill_between(x, y1)
    ax1.set_title('fill between y1 and 0')

    ax2.fill_between(x, y1, 1)
    ax2.set_title('fill between y1 and 1')

    ax3.fill_between(x, y1, y2)
    ax3.set_title('fill between y1 and y2')
    ax3.set_xlabel('x')
    fig.tight_layout()

    plt.show()

    if out:
        fig.savefig(out)
