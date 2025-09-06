
import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.use("module://mpl_ascii")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--out", type=str, required=False)
    parser.add_argument("--ascii", action="store_true")

    args = parser.parse_args()
    out = args.out
    asci = args.ascii

    if asci:
        mpl.use("module://mpl_ascii")

    x = np.linspace(0, 2*np.pi, 100)
    y = 2 * np.sin(x)

    fig, ax_dict = plt.subplot_mosaic(
        [['center', 'outward'],
        ['axes', 'data']]
    , figsize=(10,8))
    fig.suptitle('Spine positions')


    ax = ax_dict['center']
    ax.set_title("'center'")
    ax.plot(x, y)
    ax.spines[['left', 'bottom']].set_position('center')
    ax.spines[['top', 'right']].set_visible(False)

    ax = ax_dict['outward']
    ax.set_title("'outward'")
    ax.plot(x, y)
    ax.spines[['left', 'bottom']].set_position(('outward',-50))
    # ax.spines[['top', 'right']].set_visible(False)

    ax = ax_dict['axes']
    ax.set_title("'axes' (0.2, 0.2)")
    ax.plot(x, y)
    ax.spines.left.set_position(('axes', 0.2))
    ax.spines.bottom.set_position(('axes', 0.2))
    ax.spines[['top', 'right']].set_visible(False)

    ax = ax_dict['data']
    ax.set_title("'data' (1, 2)")
    ax.plot(x, y)
    ax.spines.left.set_position(('data', 1))
    ax.spines.bottom.set_position(('data', 2))
    ax.spines[['top', 'right']].set_visible(False)

    fig.tight_layout()

    plt.show()


    if out:
        fig.savefig(out)