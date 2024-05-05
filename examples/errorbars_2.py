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

    # example data
    x = np.arange(0.1, 4, 0.5)
    y = np.exp(-x)

    # example error bar values that vary with x-position
    error = 0.1 + 0.2 * x

    fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=True)
    ax0.errorbar(x, y, yerr=error, fmt='-o')
    ax0.set_title('variable, symmetric error')

    # error bar values w/ different -/+ errors that
    # also vary with the x-position
    lower_error = 0.4 * error
    upper_error = error
    asymmetric_error = [lower_error, upper_error]

    ax1.errorbar(x, y, xerr=asymmetric_error, fmt='o')
    ax1.set_title('variable, asymmetric error')
    ax1.set_yscale('log')

    if out:
        fig.savefig(out)

    plt.show()
