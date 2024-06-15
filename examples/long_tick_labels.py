import argparse
import matplotlib as mpl

import mpl_ascii

mpl.use("module://mpl_ascii")
mpl_ascii.AXES_WIDTH=60
mpl_ascii.AXES_HEIGHT=40


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--out", type=str)

    args = parser.parse_args()
    out = args.out

    import matplotlib.pyplot as plt

# Example data
    x = range(10)
    y = [i**2 for i in x]

    # Long tick labels
    x_tick_labels = [
        'This is a very long tick label 1',
        '0123456789',
        'This is a very long tick label 3',
        'This is a very long tick label 4',
        'This is a very long tick label 5',
        'This is a very long tick label 6abcde',
        'This is a very long tick label 7',
        'This is a very long tick label 8',
        'This is a very long tick label 9',
        'This is a very long tick label 10'
    ]


    y_tick_labels = [
    'Another very long tick label 1',
    'Another very long tick label 2',
    'Another very long tick label 3',
    'Another very long tick label 4',
    'Another very long tick label 5',
    ]

# Create the plot

    # Create the plot
    fig, ax = plt.subplots()
    ax.plot(x, y, marker='o')

    # Set the tick labels
    ax.set_xticks(x)
    ax.set_xticklabels(x_tick_labels, rotation=45, ha='right')

    ax.set_yticks([0,20,40,60,80])
    ax.set_yticklabels(y_tick_labels)

    # Set labels and title
    ax.set_xlabel('X Axis with Long Labels')
    ax.set_ylabel('Y Axis with Long Labels')
    ax.set_title('Plot with Long Tick Labels')

    fig.tight_layout()

    if out:
        fig.savefig(out)

    plt.show()
