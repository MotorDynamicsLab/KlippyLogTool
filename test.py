import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from matplotlib.gridspec import GridSpec
import mplcursors


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)
        self.axes = []

    def clear(self):
        self.fig.clear()
        self.axes = []

    def plot_subplots(self, plot_data):
        self.clear()
        gs = GridSpec(2, 2, figure=self.fig)  # 2行2列的GridSpec布局

        # 第一个子图，跨第一行的所有列
        ax1 = self.fig.add_subplot(gs[0, :])
        ax1.plot(plot_data[0]["x"], plot_data[0]["y"], label=plot_data[0]["label"])
        ax1.set_title(plot_data[0]["title"])
        ax1.set_xlabel(plot_data[0]["xlabel"])
        ax1.set_ylabel(plot_data[0]["ylabel"])
        ax1.legend()
        self.axes.append(ax1)

        # 第二个子图，占第二行第一列
        ax2 = self.fig.add_subplot(gs[1, 0])
        ax2.plot(plot_data[1]["x"], plot_data[1]["y"], label=plot_data[1]["label"])
        ax2.set_title(plot_data[1]["title"])
        ax2.set_xlabel(plot_data[1]["xlabel"])
        ax2.set_ylabel(plot_data[1]["ylabel"])
        ax2.legend()
        self.axes.append(ax2)

        # 第三个子图，占第二行第二列
        ax3 = self.fig.add_subplot(gs[1, 1])
        ax3.plot(plot_data[2]["x"], plot_data[2]["y"], label=plot_data[2]["label"])
        ax3.set_title(plot_data[2]["title"])
        ax3.set_xlabel(plot_data[2]["xlabel"])
        ax3.set_ylabel(plot_data[2]["ylabel"])
        ax3.legend()
        self.axes.append(ax3)

        # 为所有子图启用mplcursors显示坐标值
        mplcursors.cursor(self.axes)

        self.draw()


class ControlPanel(QWidget):
    def __init__(self, plot_data, plot_canvas):
        super().__init__()

        self.plot_data = plot_data
        self.plot_canvas = plot_canvas

        # 创建布局
        layout = QVBoxLayout()

        # 创建按钮并连接信号槽
        self.button3 = QPushButton("Generate Sine Wave")
        self.button4 = QPushButton("Generate Cosine Wave")
        self.button5 = QPushButton("Generate Linear")
        self.buttonA = QPushButton("Display Combined Plot")

        self.button3.clicked.connect(self.generate_sine_wave)
        self.button4.clicked.connect(self.generate_cosine_wave)
        self.button5.clicked.connect(self.generate_linear)
        self.buttonA.clicked.connect(self.display_combined_plot)

        # 将按钮添加到布局
        layout.addWidget(self.button3)
        layout.addWidget(self.button4)
        layout.addWidget(self.button5)
        layout.addWidget(self.buttonA)

        self.setLayout(layout)

    def show_error_message(self, error_message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error_message)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def generate_sine_wave(self):
        try:
            t = np.linspace(0, 2 * np.pi, 100)
            y = np.sin(t)
            self.plot_data.append(
                {
                    "x": t,
                    "y": y,
                    "label": "Sine Wave",
                    "title": "Sine Wave Plot",
                    "xlabel": "Time (s)",
                    "ylabel": "Amplitude",
                }
            )
            print("Sine wave generated")
        except Exception as e:
            self.show_error_message(str(e))

    def generate_cosine_wave(self):
        try:
            t = np.linspace(0, 2 * np.pi, 100)
            y = np.cos(t)
            self.plot_data.append(
                {
                    "x": t,
                    "y": y,
                    "label": "Cosine Wave",
                    "title": "Cosine Wave Plot",
                    "xlabel": "Time (s)",
                    "ylabel": "Amplitude",
                }
            )
            print("Cosine wave generated")
        except Exception as e:
            self.show_error_message(str(e))

    def generate_linear(self):
        try:
            t = np.linspace(0, 10, 100)
            y = 2 * t + 1
            self.plot_data.append(
                {
                    "x": t,
                    "y": y,
                    "label": "Linear",
                    "title": "Linear Plot",
                    "xlabel": "X-axis",
                    "ylabel": "Y-axis",
                }
            )
            print("Linear plot generated")
        except Exception as e:
            self.show_error_message(str(e))

    def display_combined_plot(self):
        try:
            if len(self.plot_data) < 3:
                raise ValueError("You need to generate at least 3 plots.")
            self.plot_canvas.plot_subplots(self.plot_data)
            print("Combined plot displayed")
        except Exception as e:
            self.show_error_message(str(e))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建主布局
        grid_layout = QGridLayout()

        # 创建PlotCanvas实例
        self.plot_canvas = PlotCanvas(self, width=5, height=4)

        # 创建保存子图数据的列表
        self.plot_data = []

        # 创建ControlPanel实例
        self.control_panel = ControlPanel(self.plot_data, self.plot_canvas)

        # 将ControlPanel和PlotCanvas添加到布局
        grid_layout.addWidget(self.control_panel, 0, 0, 1, 1)
        grid_layout.addWidget(self.plot_canvas, 1, 0, 1, 1)

        self.setLayout(grid_layout)
        self.setWindowTitle("Subplot Example")
        self.resize(600, 600)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
