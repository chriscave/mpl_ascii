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

    rng = np.random.default_rng(19680801)

    # example data
    mu = 106  # mean of distribution
    sigma = 17  # standard deviation of distribution
    x = rng.normal(loc=mu, scale=sigma, size=420)

    num_bins = 42

    fig, ax = plt.subplots()

    # the histogram of the data
    n, bins, patches = ax.hist(x, num_bins, density=True)

    # add a 'best fit' line
    y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
        np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
    ax.plot(bins, y, '--')
    ax.set_xlabel('Value')
    ax.set_ylabel('Probability density')
    ax.set_title('Histogram of normal distribution sample: '
                fr'$\mu={mu:.0f}$, $\sigma={sigma:.0f}$')

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()

    if out:
        fig.savefig(out)

    plt.show()
