# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.9.1] 2024-06-15

### Changed

- Updated tick rendering logic to prevent overlap. Xticks now alternate direction or extend downwards, with possible truncation for both xticks and yticks.
- Changed axes labels, title and legend so they are now centered.

## [0.9.0] 2024-06-11

### Added

- Add support for `figure.show()` which will now display the text plot of the figure.

## [0.8.0] 2024-06-10

### Added

- Add support for contour plots.
- Add support for text objects in plot.
- Add error handling for when the plots are not part of the library.

## [0.7.2] 2024-05-30

### Fixed

- Fixed the padding between the colorbar and the axes when saving to a txt file.

## [0.7.1] 2024-05-30

### Fixed

- Fix position of yaxis labels on colorbar axis so they are on the right side instead of the left side.

## [0.7.0] 2024-05-26

### Added

- Add support for color bars on scatter plots

## [0.6.4] 2024-05-26

### Fixed

- Add fix so if there is a `None` value in only one axis then the line plot does not raise an error and instead skips over it.

## [0.6.3] 2024-05-24

### Fixed

- Line plots now handle None values as matplotlib does. If a `None` value is passed into a line plot then it has line break.

## [0.6.2] 2024-05-19

### Fixed

- `mpl_ascii` is now compatible with matplotlib 3.9.

## [0.6.1] 2024-05-11

### Fixed

- Contour plots will return empty frame instead of raising an error.

## [0.6.0] 2024-05-10

### Added

- Add support for violin plots

### Fixed

- Fixed empty line markers with box plots.

## [0.5.0] 2024-05-10

### Added

- Added support for python 3.7+

## [0.4.0] 2024-05-05

### Added

- Added support for errorbars and line markers on line plots.

## [0.3.0] - 2024-04-30

### Added

- You can now enable/disable colors to the ascii plots by setting the global variable `mpl_ascii.ENABLE_COLOR`. It is set to `True` by default.

## [0.2.0] - 2024-04-28

### Added

- The width and height of each axes can be set using `mpl_ascii.AXES_WIDTH` and `mpl_ascii.AXES_HEIGHT`. It defaults to 150 characters in width and 40 characters in height.

## [0.1.0] - 2024-04-25

### Added

When using the `mpl_ascii` backend then `plt.show()` will print the plot as a string consisting of basic ASCII characters. This is supported for:

    - Bar charts
    - Horizontal bar charts
    - Line plots
    - Scatter plots

You can also save figures as a text file. You can do this by using the savefig `figure.savefig("my_figure.txt")` and this will save the ASCII plot as a txt file.


