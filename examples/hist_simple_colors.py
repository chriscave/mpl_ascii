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

    fig, axs = plt.subplots(1, 2, tight_layout=True)

    # N is the count in each bin, bins is the lower-limit of the bin
    N, bins, patches = axs[0].hist(dist1, bins=n_bins)

    # We'll color code by height, but you could use any scalar
    fracs = N / N.max()

    # we need to normalize the data to 0..1 for the full range of the colormap
    norm = colors.Normalize(fracs.min(), fracs.max())

    # Now, we'll loop through our objects and set the color of each accordingly
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    # We can also normalize our inputs by the total number of counts
    axs[1].hist(dist1, bins=n_bins, density=True)

    # Now we format the y-axis to display percentage
    axs[1].yaxis.set_major_formatter(PercentFormatter(xmax=1))
    if out:
        fig.savefig(out)

    plt.show()
