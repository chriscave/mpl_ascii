# mpl_ascii

A matplotlib backend that produces plots using only ASCII characters.

## Quick start

Install `mpl_ascii` using pip

```bash
pip install mpl_ascii
```

To use mpl_ascii, add to your python program

```python
import matplotlib as mpl

mpl.use("module://mpl_ascii")
```

When you use `plt.show()` then it will print the plots as strings that consists of ASCII characters.

If you want to save a figure to a `.txt` file then just use `figure.savefig("my_figure.txt")`

See more information about using backends here: https://matplotlib.org/stable/users/explain/figure/backends.html
