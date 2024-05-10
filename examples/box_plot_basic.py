import argparse
import matplotlib as mpl
import mpl_ascii

mpl.use("module://mpl_ascii")
mpl_ascii.ENABLE_COLORS=False
mpl_ascii.AXES_HEIGHT=60

if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--out", type=str)

    args = parser.parse_args()
    out = args.out

    import matplotlib.pyplot as plt
    import numpy as np

    from matplotlib.patches import Polygon

    # Fixing random state for reproducibility
    np.random.seed(19680801)

    # fake up some data
    spread = np.random.rand(50) * 100
    center = np.ones(25) * 50
    flier_high = np.random.rand(10) * 100 + 100
    flier_low = np.random.rand(10) * -100
    data = np.concatenate((spread, center, flier_high, flier_low))

    fig, axs = plt.subplots(1,3)

    # basic plot
    axs[0].boxplot(data)
    axs[0].set_title('basic plot')


    # notched plot
    axs[1].boxplot(data, 1)
    axs[1].set_title('notched plot')


    # horizontal boxes
    axs[2].boxplot(data, 0, 'rs', 0)
    axs[2].set_title('horizontal boxes')

    if out:
        fig.savefig(out)

    plt.show()