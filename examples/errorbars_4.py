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

    fig = plt.figure()
    x = np.arange(10) / 10
    y = (x + 0.1)**2
    upperlimits = [True, False] * 5
    lowerlimits = [False, True] * 5

    plt.errorbar(x, y, xerr=0.1, xlolims=True, label='xlolims=True')
    y = (x + 0.1)**3

    plt.errorbar(x + 0.6, y, xerr=0.1, xuplims=upperlimits, xlolims=lowerlimits,
                label='subsets of xuplims and xlolims')

    y = (x + 0.1)**4
    plt.errorbar(x + 1.2, y, xerr=0.1, xuplims=True, label='xuplims=True')

    plt.legend()

    if out:
        fig.savefig(out)

    plt.show()
