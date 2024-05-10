import argparse
import matplotlib as mpl
import mpl_ascii

mpl.use("module://mpl_ascii")
mpl_ascii.AXES_WIDTH=100
mpl_ascii.AXES_HEIGHT=40

if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--out", type=str)

    args = parser.parse_args()
    out = args.out

    import matplotlib.pyplot as plt

    # Example data
    fruits = ['apple', 'blueberry', 'cherry', 'orange']
    counts = [10, 15, 7, 5]
    colors = ['red', 'blue', 'red', 'orange']  # Colors corresponding to each fruit

    fig, ax = plt.subplots()

    # Plot each bar individually
    for fruit, count, color in zip(fruits, counts, colors):
        ax.bar(fruit, count, color=color, label=color)

    # Display the legend
    ax.legend(title='Fruit color')


    if out:
        fig.savefig(out)
    plt.show()