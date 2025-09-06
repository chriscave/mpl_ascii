import argparse
import matplotlib as mpl
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import numpy as np


# This demonstates
# - Barchart
#    - Data coordinate annotations on barcharts
#    - Legend width depends on legend label text
# - Scatter plot
#    - Legend width depends on legend title
# - Barchart stacked
#    - Annotations that are callable
#    - Legend without a title


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--ascii", action="store_true")
    parser.add_argument("--out", type=str, required=False)


    args = parser.parse_args()
    out = args.out
    asc = args.ascii

    if asc:
        mpl.use("module://mpl_ascii")

    fig, axes = plt.subplots(2,2, figsize=(10,8))

    # data from https://allisonhorst.github.io/palmerpenguins/
    fig.suptitle("Examples of basic plots")


    labels = ['G1', 'G2', 'G3', 'G4', 'G5']
    men_means = [20, 34, 30, 35, 27]
    women_means = [25, 32, 34, 20, 25]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    ax: Axes = axes[0,0]

    rects1 = ax.bar(x - width/2, men_means, width, label='Men')
    rects2 = ax.bar(x + width/2, women_means, width, label='Women')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scores')
    ax.set_xlabel("Groups")
    ax.set_title('Scores by group and gender')
    ax.set_xticks(x, labels)
    ax.legend(title="Gender")

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)


    ax = axes[0,1]
    np.random.seed(0)
    x = np.random.rand(40)
    y = np.random.rand(40)
    colors = np.random.choice(['red', 'green', 'blue', 'yellow'], size=40)
    color_labels = ['Red', 'Green', 'Blue', 'Yellow']  # Labels corresponding to colors

    # Create a scatter plot
    for color, label in zip(['red', 'green', 'blue', 'yellow'], color_labels):
        # Plot each color as a separate scatter plot to enable legend tracking
        idx = np.where(colors == color)
        ax.scatter(x[idx], y[idx], color=color, label=label)

    # Set title and labels

    ax.set_title('Scatter Plot with 4 Different Colors')
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')

    # Add a legend
    ax.legend(title='Point Colors')

    ax = axes[1,0]
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)
    c = 1 + np.cos(2 * np.pi * t)

    ax.plot(t, s)
    ax.plot(t, c)

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
        title='About as simple as it gets, folks')

    ax = axes[1,1]
    species = ('Adelie', 'Chinstrap', 'Gentoo')
    sex_counts = {
        'Male': np.array([73, 34, 61]),
        'Female': np.array([73, 34, 58]),
    }
    width = 0.6  # the width of the bars: can also be len(x) sequence

    bottom = np.zeros(3)

    for sex, sex_count in sex_counts.items():
        p = ax.bar(species, sex_count, width, label=sex, bottom=bottom)
        bottom += sex_count

        ax.bar_label(p, label_type='center')

    ax.set_title('Number of penguins by sex')
    ax.legend()
    ax.set_xlabel("Penguines")
    ax.set_ylabel("Count")


    fig.tight_layout()


    plt.show()

    if out:
        fig.savefig(out)
