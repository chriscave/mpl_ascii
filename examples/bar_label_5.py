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

    animal_names = ['Lion', 'Gazelle', 'Cheetah']
    mph_speed = [50, 60, 75]

    fig, ax = plt.subplots()
    bar_container = ax.bar(animal_names, mph_speed)
    ax.set(ylabel='speed in MPH', title='Running speeds', ylim=(0, 80))

    # ax.bar_label(bar_container, fmt=lambda x: f'{x * 1.61:.1f} km/h')

    if out:
        fig.savefig(out)

    plt.show()
