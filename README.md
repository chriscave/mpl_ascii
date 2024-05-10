# mpl_ascii

A matplotlib backend that produces plots using only ASCII characters. It is available for python 3.7+.

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

## Examples

### Bar chart

The following is taken from the example in `examples/bar_color.py`

```python
import matplotlib.pyplot as plt
import matplotlib as mpl
import mpl_ascii

mpl_ascii.AXES_WIDTH=100
mpl_ascii.AXES_HEIGHT=40

mpl.use("module://mpl_ascii")

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

plt.show()
```

![bar chart with color](https://imgur.com/u4pRU3E.png)

### Scatter plot

The following is taken from the example in `examples/scatter_multi_color.py`

```python
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import mpl_ascii

mpl_ascii.AXES_WIDTH=100
mpl_ascii.AXES_HEIGHT=40


mpl.use("module://mpl_ascii")

np.random.seed(0)
x = np.random.rand(40)
y = np.random.rand(40)
colors = np.random.choice(['red', 'green', 'blue', 'yellow'], size=40)
color_labels = ['Red', 'Green', 'Blue', 'Yellow']  # Labels corresponding to colors

# Create a scatter plot
fig, ax = plt.subplots()
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
plt.show()
```

![Scatter plot with color](https://imgur.com/6LOv6L3.png)

### Line plot

The following is taken from the example in `examples/double_plot.py`


```python
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import mpl_ascii

mpl_ascii.AXES_WIDTH=100
mpl_ascii.AXES_HEIGHT=40


mpl.use("module://mpl_ascii")


# Data for plotting
t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2 * np.pi * t)
c = 1 + np.cos(2 * np.pi * t)

fig, ax = plt.subplots()
ax.plot(t, s)
ax.plot(t, c)

ax.set(xlabel='time (s)', ylabel='voltage (mV)',
    title='About as simple as it gets, folks')

plt.show()
```
![Double plot with colors](https://imgur.com/PyTPR4C.png)

You can find more examples and their outputs in the `examples` folder.

## Global Variables

### mpl_ascii.AXES_WIDTH

Adjust the width of each axis according to the number of characters. The final width of the image might extend a few characters beyond this, depending on the size of the ticks and axis labels. Default is `150`.

### mpl_ascii.AXES_HEIGHT

Adjust the height of each axis according to the number of characters. The final height of the image might extend a few characters beyond this, depending on the size of the ticks and axis labels. Default is `40`

### mpl_ascii.ENABLE_COLORS

Executing `plt.show()` will render the image in colored text. Default is `True`


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