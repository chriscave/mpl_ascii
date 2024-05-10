import argparse
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np


mpl.use("module://mpl_ascii")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--out", type=str)

    args = parser.parse_args()
    out = args.out

    fig, ax = plt.subplots()

    # Fixing random state for reproducibility
    np.random.seed(19680801)


    # generate some random test data
    all_data = [np.random.normal(0, std, 100) for std in range(6, 10)]

    # plot violin plot
    ax.violinplot(all_data,
                    showmeans=False,
                    showmedians=True)
    ax.set_title('Violin plot')

    # adding horizontal grid lines
    ax.yaxis.grid(True)
    ax.set_xticks([y + 1 for y in range(len(all_data))],
                labels=['x1', 'x2', 'x3', 'x4'])
    ax.set_xlabel('Four separate samples')
    ax.set_ylabel('Observed values')


    if out:
        fig.savefig(out)

    plt.show()