import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QPushButton,
    QMessageBox,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


import mplcursors
from model.main_model import MainViewModel, Utilities


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)
        self.axes = []

    def clear(self, plot_data):
        if plot_data is not None:
            plot_data.clear()
        self.axes = []
        self.fig.clear()

    def common_configure_subplot(self, list_dict):
        data = list_dict[0]
        row, col, index = data["subplots"]
        ax = self.fig.add_subplot(row, col, index)
        ax.set_title(data["title"])
        ax.set_xlabel(data["xlabel"])
        ax.set_ylabel(data["ylabel"])
        return ax

    def plot_subplots(self, plot_data_list):
        for list_dict in plot_data_list:
            ax = self.common_configure_subplot(list_dict)
            for index, dict in enumerate(list_dict):
                if index == 0:
                    continue  # 跳过第一项
                ax.plot(
                    dict["x"],
                    dict["y"],
                    label=dict["label"],
                    color=dict["color"],
                    linestyle=dict["linestyle"],
                )
                ax.legend(loc="upper right")
                self.axes.append(ax)

        mplcursors.cursor(self.axes, hover=True)
        self.draw()


class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.plot_data = []
        self.file_paths = ["logs/klippy8.log"]

        self.viewModel = MainViewModel()
        grid_layout = QGridLayout()

        # 第一行两个按钮
        self.open_log_btn = QPushButton("选择log")
        self.open_log_btn.clicked.connect(self.open_log)
        grid_layout.addWidget(self.open_log_btn, 0, 0, 1, 3)  # 占用一行的三列

        # 第二行三个按钮
        self.comprehensive_analysis_btn = QPushButton("综合分析")
        self.comprehensive_analysis_btn.clicked.connect(self.comprehensive_analysis)
        grid_layout.addWidget(self.comprehensive_analysis_btn, 1, 0)

        self.loss_packet_analysis_btn = QPushButton("丢包分析")
        self.loss_packet_analysis_btn.clicked.connect(self.loss_packet_analysis)
        grid_layout.addWidget(self.loss_packet_analysis_btn, 1, 1)

        self.loss_packet_monitor_btn = QPushButton("丢包监控")
        self.loss_packet_monitor_btn.clicked.connect(self.loss_packet_monitor)
        grid_layout.addWidget(self.loss_packet_monitor_btn, 1, 2)

        # 剩下的位置放一个画布容器
        self.plot_canvas = PlotCanvas(self, width=5, height=4)
        grid_layout.addWidget(self.plot_canvas, 2, 0, 1, 3)

        self.setLayout(grid_layout)
        self.resize(600, 400)

    # 功能函数
    @staticmethod
    def show_error_msg(error):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    # 事件处理
    def open_log(self):
        self.file_paths = Utilities.get_file_paths(self)
        self.plot_canvas.clear(self.plot_data)

    def comprehensive_analysis(self):

        if len(self.file_paths) > 0:
            log = ""
            with open(self.file_paths[0], "r", encoding="utf-8") as file:
                log = file.read()

            self.viewModel.output_analysis_result(log)
            self.plot_data = self.viewModel.comprehensive_analysis(log)
            self.plot_canvas.plot_subplots(self.plot_data)
        else:
            ControlPanel.show_error_msg("未打开log文件")

    def loss_packet_analysis(self):
        pass

    def loss_packet_monitor(self):
        pass


class MainPanel(QWidget):
    def __init__(self):
        super().__init__()

        # 创建主布局
        grid_layout = QGridLayout()

        # 创建保存子图数据的列表
        self.plot_data = []

        # 创建ControlPanel实例
        self.control_panel = ControlPanel()

        # 将ControlPanel
        grid_layout.addWidget(self.control_panel, 0, 0, 1, 1)

        self.setLayout(grid_layout)
        self.setWindowTitle("Subplot Example")
        self.resize(600, 600)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainPanel()
    main_window.show()
    sys.exit(app.exec_())
