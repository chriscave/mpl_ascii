# mpl_ascii

A matplotlib backend that produces plots using only ASCII characters. It is available for python 3.10+.

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

## Example

The following is taken from the example in `examples/bar_color.py`

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

fruits = ['apple', 'blueberry', 'cherry', 'orange']
counts = [40, 100, 30, 55]
bar_labels = ['red', 'blue', '_red', 'orange']
bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']

ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

ax.set_ylabel('fruit supply')
ax.set_title('Fruit supply by kind and color')
ax.legend(title='Fruit color')

plt.show()
```

You can find more examples in the `examples` folder and their txt files under `tests/accept`.

## Use cases

### Using Version Control for Plots

Handling plots with version control can pose challenges, especially when dealing with binary files. Here are some issues you might encounter:

- Binary Files: Committing binary files like PNGs can significantly increase your repository’s size. They are also difficult to compare (diff) and can lead to complex merge conflicts.

- SVG Files: Although SVGs are more version control-friendly than binary formats, they can still cause problems:
    - Large or complex graphics can result in excessively large SVG files.
    - Diffs can be hard to interpret.

To mitigate these issues, ASCII plots serve as an effective alternative:

- Size: ASCII representations are much smaller in size.
- Version Control Compatibility: They are straightforward to diff and simplify resolving merge conflicts.


This package acts as a backend for Matplotlib, enabling you to continue creating plots in your usual formats (PNG, SVG) during development. When you’re ready to commit your plots to a repository, simply switch to the `mpl_ascii` backend to convert them into ASCII format.

## Feedback

Please help make this package better by:
- reporting bugs.
- making feature requests. Matplotlib is an enormous library and this supports only a part of it. Let me know if there particular charts that you would like to be converted to ASCII
- letting me know what you use this for.

If you want to tell me about any of the above just use the Issues tab for now.

Thanks for reading and I hope you will like these plots as much as I do :-)