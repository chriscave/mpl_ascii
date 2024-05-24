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

    fig, ax = plt.subplots()

    ax.plot([0, 0, None, 1, 1], [0, 1, None, 0, 1])

    if out:
        fig.savefig(out)

    plt.show()
