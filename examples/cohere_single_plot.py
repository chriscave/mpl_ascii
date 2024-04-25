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

    np.random.seed(19680801)

    dt = 0.01
    t = np.arange(0, 30, dt)
    nse1 = np.random.randn(len(t))                 # white noise 1
    nse2 = np.random.randn(len(t))                 # white noise 2

    # Two signals with a coherent part at 10 Hz and a random part
    s1 = np.sin(2 * np.pi * 10 * t) + nse1
    s2 = np.sin(2 * np.pi * 10 * t) + nse2

    fig, axs = plt.subplots(layout='constrained')
    axs.plot(t, s1, t, s2)
    axs.set_xlim(0, 2)
    axs.set_xlabel('Time (s)')
    axs.set_ylabel('s1 and s2')
    axs.grid(True)

    # cxy, f = axs[1].cohere(s1, s2, 256, 1. / dt)
    # axs[1].set_ylabel('Coherence')

    if out:
        fig.savefig(out)

    plt.show()
