import mplcursors
from matplotlib.figure import Figure
import matplotlib.font_manager as fm
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        font_path = "C:/Windows/Fonts/simhei.ttf"  # TODO, placed in setting to read
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.prop = fm.FontProperties(fname=font_path)
        self.setParent(parent)
        self.axes = []
        self.lines = []

    def clear(self, plot_data):
        if plot_data is not None and len(plot_data) != 0:
            plot_data.clear()
        self.axes = []
        self.fig.clear()

    def common_configure_subplot(self, list_dict):
        data = list_dict[0]
        row, col, index = data["subplots"]
        ax = self.fig.add_subplot(row, col, index)
        ax.set_title(data["title"], fontproperties=self.prop)
        ax.set_xlabel(data["xlabel"], fontproperties=self.prop)
        ax.xaxis.set_label_coords(-0.04, -0.04)
        ax.set_ylabel(data["ylabel"], fontproperties=self.prop)
        return ax

    def set_line_visible(self, label, visible):
        for ax, line in self.lines:
            if line.get_gid() == label:
                line.set_visible(visible)  # Toggle line visibility
                break
        self.draw()

    def plot_subplots(self, plot_data_list):
        self.lines.clear()
        for list_dict in plot_data_list:
            ax = self.common_configure_subplot(list_dict)
            for index, dict in enumerate(list_dict):
                if index == 0:
                    continue  # skip first item
                (line,) = ax.plot(
                    dict["x"],
                    dict["y"],
                    label=dict["label"],
                    color=dict["color"],
                    linestyle=dict["linestyle"],
                )
                ax.legend(loc="upper right", prop=self.prop)
                self.axes.append(ax)
                line.set_gid(dict["label"])  # Set the line's label to the group ID
                self.lines.append((ax, line))  # Store axes and lines

        cursor = mplcursors.cursor(self.axes, hover=True)

        @cursor.connect("add")
        def on_add(sel):
            x, y = sel.target
            line = sel.artist
            label = line.get_label()
            sel.annotation.set_text(f"{label}\nX: {x}\nY: {y}")
            sel.annotation.set_fontproperties(self.prop)

        self.draw()
