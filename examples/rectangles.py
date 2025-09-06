import argparse
import matplotlib as mpl
import matplotlib.patches as patches
from matplotlib import colors
import matplotlib.pyplot as plt
import numpy as np

# This demonstrates:
# - a horizontal bar chart with error bars that
#   have black color originally but is now displayed as white
# - a histogram with narrow bars with a long y label
# - Rectangles rotatedt
#   - use a character for lines that is auto assigned and not overriden.
#   - Has fill but no line color.

if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--out", type=str, required=False)
    parser.add_argument("--ascii", action="store_true")

    args = parser.parse_args()
    out = args.out
    asci = args.ascii

    if asci:
        mpl.use("module://mpl_ascii")


    # Fixing random state for reproducibility
    np.random.seed(19680801)

    fig, axes = plt.subplots(2,2, figsize=(10,8))

    fig.suptitle("It's all about rectangles")


    ax = axes[0,0]
    people = ('Tom', 'Dick', 'Harry', 'Slim', 'Jim')
    y_pos = np.arange(len(people))
    performance = 3 + 10 * np.random.rand(len(people))
    error = np.random.rand(len(people))

    ax.barh(y_pos, performance, xerr=error, align='center')

    ax.set_yticks(y_pos, labels=people)
    ax.invert_yaxis()
    ax.set_xlabel('Performance')
    ax.set_title('My horizontal bar chart with error bars')

    rng = np.random.default_rng(19680801)


    mu = 106
    sigma = 17
    x = rng.normal(loc=mu, scale=sigma, size=420)

    num_bins = 42

    ax = axes[0,1]
    n, bins, p = ax.hist(x, num_bins, density=True)


    y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
        np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
    ax.plot(bins, y, '--')
    ax.set_xlabel('Value')
    ax.set_ylabel('Probability density')
    ax.set_title('Histogram of normal distribution sample: '
                fr'$\mu={mu:.0f}$, $\sigma={sigma:.0f}$')



    rect1 = patches.Rectangle(
        (0.3, 0.3),
        0.4,
        0.2,
        angle=30,
        linewidth=2,
        edgecolor='blue',
        facecolor='orange',
    )
    rect2 = patches.Rectangle(
    (0.6, 0.6),
    0.3,
    0.15,
    angle=-10,
    edgecolor="none",
    facecolor="green",
    alpha=0.5
)


    ax = axes[1,0]
    ax.add_patch(rect1)
    ax.add_patch(rect2)
    ax.set_title("Rotated Rectangles")



    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')

    rng = np.random.default_rng(19680801)

    N_points = 100000
    n_bins = 20


    dist1 = rng.standard_normal(N_points)
    dist2 = 0.4 * rng.standard_normal(N_points) + 5

    ax = axes[1,1]
    ax.set_title("Colorful Histograms")



    N, bins, patches = ax.hist(dist1, bins=n_bins)


    fracs = N / N.max()



    norm = colors.Normalize(fracs.min(), fracs.max())


    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)


    fig.tight_layout()

    plt.show()

    if out:
        fig.savefig(out)