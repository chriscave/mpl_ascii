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
```
                                                      Fruit supply by kind and color

      +----------------------------------------------------------------------------------------------------+
      |                                                                                                    |
      |                                                                                                    |
  100--                                                                                                    |
      |                            %%%%%%%%%%%%%%%%%%%                                                     |
      |                            %%%%%%%%%%%%%%%%%%%                                                     |
      |                            %%%%%%%%%%%%%%%%%%%                                                     |
      |                            %%%%%%%%%%%%%%%%%%%                                                     |
      |                            %%%%%%%%%%%%%%%%%%%                                                     |
      |                            %%%%%%%%%%%%%%%%%%%                                                     |
   80--                            %%%%%%%%%%%%%%%%%%%                                                     |
      |                            %%%%%%%%%%%%%%%%%%%                                                     |
      |                            %%%%%%%%%%%%%%%%%%%                                                     |
      |                            %%%%%%%%%%%%%%%%%%%                                                     |
      |                            %%%%%%%%%%%%%%%%%%%                                                     |
      |                            %%%%%%%%%%%%%%%%%%%                                                     |
      |                            %%%%%%%%%%%%%%%%%%%                                                     |
      |                            %%%%%%%%%%%%%%%%%%%                                                     |
   60--                            %%%%%%%%%%%%%%%%%%%                                                     |
      |                            %%%%%%%%%%%%%%%%%%%                                                     |
      |                            %%%%%%%%%%%%%%%%%%%                                                     |
f     |                            %%%%%%%%%%%%%%%%%%%                             &&&&&&&&&&&&&&&&&&&     |
r     |                            %%%%%%%%%%%%%%%%%%%                             &&&&&&&&&&&&&&&&&&&     |
u     |                            %%%%%%%%%%%%%%%%%%%                             &&&&&&&&&&&&&&&&&&&     |
i     |                            %%%%%%%%%%%%%%%%%%%                             &&&&&&&&&&&&&&&&&&&     |
t  40--                            %%%%%%%%%%%%%%%%%%%                             &&&&&&&&&&&&&&&&&&&     |
      |     ###################    %%%%%%%%%%%%%%%%%%%                             &&&&&&&&&&&&&&&&&&&     |
s     |     ###################    %%%%%%%%%%%%%%%%%%%                             &&&&&&&&&&&&&&&&&&&     |
u     |     ###################    %%%%%%%%%%%%%%%%%%%                             &&&&&&&&&&&&&&&&&&&     |
p     |     ###################    %%%%%%%%%%%%%%%%%%%                             &&&&&&&&&&&&&&&&&&&     |
p     |     ###################    %%%%%%%%%%%%%%%%%%%     ###################     &&&&&&&&&&&&&&&&&&&     |
l     |     ###################    %%%%%%%%%%%%%%%%%%%     ###################     &&&&&&&&&&&&&&&&&&&     |
y     |     ###################    %%%%%%%%%%%%%%%%%%%     ###################     &&&&&&&&&&&&&&&&&&&     |
   20--     ###################    %%%%%%%%%%%%%%%%%%%     ###################     &&&&&&&&&&&&&&&&&&&     |
      |     ###################    %%%%%%%%%%%%%%%%%%%     ###################     &&&&&&&&&&&&&&&&&&&     |
      |     ###################    %%%%%%%%%%%%%%%%%%%     ###################     &&&&&&&&&&&&&&&&&&&     |
      |     ###################    %%%%%%%%%%%%%%%%%%%     ###################     &&&&&&&&&&&&&&&&&&&     |
      |     ###################    %%%%%%%%%%%%%%%%%%%     ###################     &&&&&&&&&&&&&&&&&&&     |
      |     ###################    %%%%%%%%%%%%%%%%%%%     ###################     &&&&&&&&&&&&&&&&&&&     |
      |     ###################    %%%%%%%%%%%%%%%%%%%     ###################     &&&&&&&&&&&&&&&&&&&     |
    0--     ###################    %%%%%%%%%%%%%%%%%%%     ###################     &&&&&&&&&&&&&&&&&&&     |
      +--------------|-----------------------|----------------------|-----------------------|--------------+
                 apple               blueberry                 cherry                  orange


                                                      +-------------+
                                                      | Fruit color |
                                                      |             |
                                                      | ### red     |
                                                      | %%% blue    |
                                                      | &&& orange  |
                                                      +-------------+
```

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
```
                                                      Scatter Plot with 4 Different Colors

       +----------------------------------------------------------------------------------------------------+
       |                                                                                                    |
   1.0--                                                                                                    |
       |                            z                 v         z                                           |
       |                                                                                                    |
       |                                                                                                    |
       |                                                                                                    |
       |                                                                                                    |
       |                                                    x                                               |
       |                x                                                                                   |
   0.8--                                                                                                    |
       |                                                                                                    |
       |    x                                                                                               |
       |                                                                                                    |
       |                                                           z                                        |
       |     *                                    z   z                z                                    |
       |                                                                                                    |
   0.6--                                                        z                                           |
       |                                                                             *                      |
       |                                                                                                    |
       |                                                                                                    |
Y      |                                                                                                    |
       |                                                                           vv                       |
a      |                                                    v                 v                             |
x      |                                                                                                    |
i  0.4--                                                                                                    |
s      |                                       x              v        x                                    |
       |                                                                                                    |
       |                                                                                             z      |
       |                                                            x                              v        |
       |                                                                                 x                  |
       |                                                                                    v               |
   0.2--         *    z                             v                                                       |
       |                                                                                                    |
       |           v                                                                                  z     |
       |                                                             *     x        v         v             |
       |                                          v                                   x           vv        |
       |                                                      v                                             |
       |                                                             x                                      |
       |                                                                                                    |
   0.0--                                                                                                    |
       +---|-----------------|------------------|------------------|------------------|------------------|--+
         0.0               0.2                0.4                0.6                0.8                1.0
                                                          X axis

                                                      +--------------+
                                                      | Point Colors |
                                                      |              |
                                                      | xxx Red      |
                                                      | *** Green    |
                                                      | vvv Blue     |
                                                      | zzz Yellow   |
                                                      +--------------+
```

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

```
                                                       About as simple as it gets, folks

        +----------------------------------------------------------------------------------------------------+
        |                                                                                                    |
        |                                                                                                    |
   2.00--    ooo       +++++                             ooooo      +++++                             oo     |
        |       oo    ++   ++                           o    oo    ++   ++                           oo      |
        |        o   +      +                          o      o   +       +                         o        |
        |         o ++       +                        oo       o  +       ++                       oo        |
   1.75--         o +         +                       o         o+         +                       o         |
        |          o          ++                     o          oo         ++                     oo         |
        |         + o          +                    o           +o          +                     o          |
        |         + o           +                   o          +  o          +                   o           |
        |         +  o          +                  o           +  o          +                   o           |
   1.50--        +   o          +                  o          +   o           +                 o            |
        |        +    o          +                 o          +    o          +                 o            |
        |       +     o          +                o          +     o           +               o             |
        |       +      o          +               o          +      o          +               o             |
   1.25--      +       o          +              o           +      o           +             o              |
        |      +       o           +             o          +        o          +             o              |
        |     +         o          +            o           +        o          +             o              |
        |     +         o           +           o          +          o          +           o               |
        |    +           o          +          o           +          o          +           o               |
v  1.00--    +           o           +         o           +          o           +          o               |
o       |                o           +         o          +           o           +         o          +     |
l       |                 o          +         o          +            o          +         o          +     |
t       |                 o          +        o          +             o           +       o           +     |
a  0.75--                  o          +       o          +              o          +       o          +      |
g       |                  o          +      o          +               o           +     o           +      |
e       |                   o          +     o          +                o          +     o          +       |
        |                   o          +    o           +                o           +   o           +       |
(  0.50--                   o           +   o          +                  o          +   o          +        |
m       |                    o          +  o           +                  o          +   o          +        |
V       |                    o           + o          +                    o          + o          +         |
)       |                     o          +o           +                    o          + o          +         |
        |                     oo          o          +                     oo          o          ++         |
   0.25--                      o         o+         +                       o         o +         +          |
        |                       o       oo +       ++                        o       oo ++       +           |
        |                       o       o   +      +                          o      o   +      +            |
        |                        oo   oo    ++    ++                          oo    oo   ++    ++            |
   0.00--                         ooooo       ++++                              oooo       ++++              |
        |                                                                                                    |
        |                                                                                                    |
        +----|-----------|----------|----------|-----------|----------|----------|-----------|----------|----+
          0.00        0.25       0.50       0.75        1.00       1.25       1.50        1.75       2.00
                                                           time (s)
```

You can find more examples and their outputs in the `examples` folder.

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