from matplotlib._pylab_helpers import Gcf

from matplotlib.backends.backend_agg import (
    FigureManagerBase,
    RendererAgg,
    FigureCanvasAgg,
)
from matplotlib.collections import PathCollection
from matplotlib.container import BarContainer
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
import numpy as np

from mpl_ascii.ascii_canvas import AsciiCanvas
from mpl_ascii.color_map import map_color_to_ascii
from mpl_ascii.draw import draw_bar, draw_frame, draw_line, draw_x_ticks, draw_y_ticks
from mpl_ascii.tools import linear_transform

AXES_WIDTH = 150
AXES_HEIGHT = 40

class RendererAscii(RendererAgg):

    def __init__(self, width, height, dpi):
        super(RendererAscii, self).__init__(width, height, dpi)
        self.texts = []
        self.tick_info = []

    def clear(self):
        super(RendererAscii, self).clear()
        self.texts = []
        self.tick_info = []

    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        super(RendererAscii, self).draw_text(
            gc, x, y, s, prop, angle, ismath=ismath, mtext=mtext
        )

        if mtext is not None:
            self.texts.append(mtext)


def show():
    for manager in Gcf.get_all_fig_managers():
        canvas = manager.canvas
        canvas.draw()
        string = canvas.to_txt()
        print(string)


class FigureCanvasAscii(FigureCanvasAgg):

    def __init__(self, figure: Figure | None = ...) -> None:
        super().__init__(figure)
        self.tick_info = []

    def get_renderer(self):
        w, h = self.figure.bbox.size
        key = w, h, self.figure.dpi
        reuse_renderer = self._lastKey == key
        if not reuse_renderer:
            self.renderer = RendererAscii(w, h, self.figure.dpi)
            self._lastKey = key
        return self.renderer

    def to_txt(self, sep="\n", tw=240, invert=False, threshold=200):
        self.draw()

        figure = self.figure

        axes_height = AXES_HEIGHT
        axes_width = AXES_WIDTH

        frame_buffer_left = 1
        frame_buffer_right = 1
        frame_buffer_top = 1
        frame_buffer_bottom = 1


        frame_width = axes_width + frame_buffer_left + frame_buffer_right
        frame_height = axes_height + frame_buffer_top + frame_buffer_bottom

        ascii_canvases = []
        for ax in figure.axes:
            color_to_ascii = map_color_to_ascii(ax)

            x_range = ax.get_xlim()
            if x_range[1] < x_range[0]:
                x_range = x_range[1], x_range[0]

            y_range = ax.get_ylim()
            if y_range[1] < y_range[0]:
                y_range = y_range[1], y_range[0]

            x_min, x_max = x_range
            y_min, y_max = y_range

            canvas = AsciiCanvas(np.full((axes_height, axes_width), fill_value=" "))

            all_bars = []

            for container in ax.containers:
                if not isinstance(container, BarContainer):
                    continue
                for bar in container.patches:
                    if not isinstance(bar, Rectangle):
                        continue
                    all_bars.append(bar)

            for bar in all_bars:
                char = color_to_ascii[bar.get_facecolor()]

                canvas_bar = AsciiCanvas(
                        draw_bar(
                        bar.get_height(),
                        bar.get_width(),
                        axes_height,
                        axes_width,
                        x_range,
                        y_range,
                        char
                    )
                )

                ascii_x_bar = round(linear_transform(bar.xy[0], x_min, x_max, 0, axes_width-1))
                ascii_y_bar = round(linear_transform(bar.xy[1], y_min, y_max, 1, axes_height))

                canvas = canvas.update(canvas_bar, (axes_height - ascii_y_bar - canvas_bar.shape[0]+1, ascii_x_bar))

            for line in ax.get_lines():
                char = color_to_ascii[line.get_color()]
                xy_data = line.get_xydata()
                x_data, y_data = [dat[0] for dat in xy_data], [dat[1] for dat in xy_data]

                line = AsciiCanvas(
                        draw_line(
                        width=axes_width,
                        height=axes_height,
                        x_data=x_data,
                        y_data=y_data,
                        x_range=x_range,
                        y_range=y_range,
                        char = char
                    )
                )

                canvas = canvas.update(line, (0,0))

            for collection in ax.collections:
                if not isinstance(collection, PathCollection):
                    continue
                offsets = collection.get_offsets()

                color = collection.get_facecolors()[0]
                for point in offsets:
                    color = tuple(color)

                    x_new = round(linear_transform(point[0], x_min, x_max, 0, axes_width-1))
                    y_new = round(linear_transform(point[1], y_min, y_max, 1, axes_height))

                    canvas = canvas.update(AsciiCanvas(np.array([[color_to_ascii[color]]])), (axes_height-y_new, x_new))



            # for text in ax.texts:
            #     text_canvas = AsciiCanvas(np.array([list(text.get_text())]))
            #     ascii_x = round(linear_transform(text.xy[0], x_min, x_max, 0, axes_width-1))
            #     ascii_y = round(linear_transform(text.xy[1], y_min, y_max, 1, axes_height))
            #     canvas = canvas.update(text_canvas, (axes_height - ascii_y, ascii_x))

            canvas = canvas.update(AsciiCanvas(draw_frame(frame_height, frame_width)), (-frame_buffer_left,-frame_buffer_top))

            tick_data = [tick.get_position()[0] for tick in ax.xaxis.get_ticklabels()]
            label_data = [tick.get_text().replace("\n", "") for tick in ax.xaxis.get_ticklabels()]
            xticks = AsciiCanvas(draw_x_ticks(axes_width, tick_data, label_data, x_range))

            xlabel = AsciiCanvas(np.array([list(ax.get_xlabel())]))

            xticks_and_label = xticks.update(xlabel, location=(xticks.shape[0],int(xticks.shape[1] / 2)))

            canvas = canvas.update(xticks_and_label, location=(canvas.shape[0]-1, 1))

            tick_data = [tick.get_loc() for tick in ax.yaxis.get_major_ticks()]
            label_data = [tick.label1.get_text().replace("\n", "") for tick in ax.yaxis.get_major_ticks()]
            yticks = AsciiCanvas(draw_y_ticks(axes_height, tick_data, label_data, y_range))

            ylabel = AsciiCanvas(np.array([list(ax.get_ylabel())]).T)
            yticks_and_label = yticks.update(ylabel, location=(int(yticks.shape[0] / 2), -(ylabel.shape[1] + 1)))

            canvas = canvas.update(yticks_and_label, location=(1, -yticks_and_label.shape[1]+1))


            ax_title = AsciiCanvas(np.array([list(ax.get_title())]))
            canvas = canvas.update(ax_title, location=(-(ax_title.shape[0] + 1), int(canvas.shape[1] / 2)))

            legend = ax.get_legend()
            if legend:
                handles, text = legend.legendHandles, legend.texts

                canvas_legend = AsciiCanvas()
                for handle, text in zip(handles, text):
                    char = " "
                    if isinstance(handle, Rectangle):
                        char = color_to_ascii[handle.get_facecolor()]
                    if isinstance(handle, Line2D):
                        char = color_to_ascii[handle.get_color()]
                    if isinstance(handle, PathCollection):
                        color = tuple(handle.get_facecolor()[0])
                        char = color_to_ascii[color]

                    arr = np.array([[char] * 3 + [" "] + list(text.get_text())])
                    canvas_legend = canvas_legend.update(AsciiCanvas(arr), (canvas_legend.shape[0], 0))

                title = legend.get_title().get_text() or "Legend"
                title = AsciiCanvas(np.array([list(title)]))
                canvas_legend = canvas_legend.update(title, (-2,0))
                legend_frame = AsciiCanvas(draw_frame(canvas_legend.shape[0]+2, canvas_legend.shape[1]+4))
                canvas_legend = legend_frame.update(canvas_legend, (1,2))

                canvas = canvas.update(canvas_legend, (canvas.shape[0] + 1, round(canvas.shape[1] / 2) ))

            ascii_canvases.append(canvas)

        image_canvas = AsciiCanvas()
        for canvas in ascii_canvases:
            image_canvas = image_canvas.update(canvas, (image_canvas.shape[0], 0))

        return str(image_canvas)


    def print_txt(self, filename, **kwargs):
        if isinstance(filename, str):
            with open(filename, "w") as f:
                f.write(self.to_txt())
        else:
            filename.write(self.to_txt().encode())


FigureCanvas = FigureCanvasAscii
FigureManager = FigureManagerBase
