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

    fruit_names = ['Coffee', 'Salted Caramel', 'Pistachio']
    fruit_counts = [4000, 2000, 7000]

    fig, ax = plt.subplots()
    bar_container = ax.bar(fruit_names, fruit_counts)
    ax.set(ylabel='pints sold', title='Gelato sales by flavor', ylim=(0, 8000))
    ax.bar_label(bar_container, fmt='{:,.0f}')

    if out:
        fig.savefig(out)

    plt.show()
