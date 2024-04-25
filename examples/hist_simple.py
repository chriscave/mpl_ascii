import argparse
import matplotlib as mpl

mpl.use("module://mpl_ascii")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--out", type=str)

    args = parser.parse_args()
    out = args.out

    # data from https://allisonhorst.github.io/palmerpenguins/

    import matplotlib.pyplot as plt
    import numpy as np

    from matplotlib import colors
    from matplotlib.ticker import PercentFormatter

    # Create a random number generator with a fixed seed for reproducibility
    rng = np.random.default_rng(19680801)

    N_points = 100000
    n_bins = 20

    # Generate two normal distributions
    dist1 = rng.standard_normal(N_points)
    dist2 = 0.4 * rng.standard_normal(N_points) + 5

    fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)

    # We can set the number of bins with the *bins* keyword argument.
    axs[0].hist(dist1, bins=n_bins)
    axs[1].hist(dist2, bins=n_bins)

    if out:
        fig.savefig(out)

    plt.show()
