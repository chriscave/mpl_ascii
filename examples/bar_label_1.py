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

    species = ('Adelie', 'Chinstrap', 'Gentoo')
    sex_counts = {
        'Male': np.array([73, 34, 61]),
        'Female': np.array([73, 34, 58]),
    }
    width = 0.6  # the width of the bars: can also be len(x) sequence


    fig, ax = plt.subplots()
    bottom = np.zeros(3)

    for sex, sex_count in sex_counts.items():
        p = ax.bar(species, sex_count, width, label=sex, bottom=bottom)
        bottom += sex_count

        ax.bar_label(p, label_type='center')

    ax.set_title('Number of penguins by sex')
    ax.legend()

    if out:
        fig.savefig(out)

    plt.show()
