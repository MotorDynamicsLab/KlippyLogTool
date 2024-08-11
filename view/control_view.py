from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QPushButton,
    QMessageBox,
    QMainWindow,
    QVBoxLayout,
    QAction,
    QTextEdit,
    QScrollArea,
    QLabel,
    QInputDialog,
)
import mplcursors


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)
        self.axes = []

    def clear(self, plot_data):
        if plot_data is not None and len(plot_data) != 0:
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
        self.file_paths = ["logs/klippy.log"]

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
        self.container = QWidget(self)
        grid_layout.addWidget(self.container, 2, 0, 1, 3)

        # 临时借用的容器布局 和 其他
        self.container_layout = QVBoxLayout(self.container)
        self.file_index = 0
        self.fun = None

        # 图切换按键
        self.button_prev = QPushButton("<")
        self.button_next = QPushButton(">")
        self.button_prev.setFixedSize(30, 30)
        self.button_next.setFixedSize(30, 30)
        self.button_prev.clicked.connect(self.show_previous_plot)
        self.button_next.clicked.connect(self.show_next_plot)

        self.convas_gird = QGridLayout()
        self.convas_gird.addWidget(self.button_prev, 0, 0)
        self.convas_gird.addWidget(self.button_next, 0, 2)
        self.setLayout(grid_layout)

    # 功能函数
    @staticmethod
    def show_error_msg(error):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def clear_container(self):
        for i in reversed(range(self.container_layout.count())):
            widget = self.container_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def save_some_files(self, only_cfg=False):
        log = ""
        with open(self.file_paths[0], "r", encoding="utf-8") as file:
            log = file.read()

        if only_cfg:
            self.viewModel.output_analysis_result(log)
        else:
            self.viewModel.output_cfg(log)

    # 事件处理
    def open_log(self):
        self.file_paths = Utilities.get_file_paths(self)
        self.file_index = 0

    def comprehensive_analysis(self):

        if self.fun is None or self.fun != self.comprehensive_analysis:
            self.fun = self.comprehensive_analysis
            self.clear_container()

            # 做一个组件，让布局可以包含进去
            canvas_widget = QWidget(self)
            canvas_widget.setLayout(self.convas_gird)
            self.plot_canvas = PlotCanvas(self, width=5, height=8)
            self.convas_gird.addWidget(self.plot_canvas, 0, 1)
            self.container_layout.addWidget(canvas_widget)

        if self.plot_canvas is not None:
            self.plot_canvas.clear(self.plot_data)
            if len(self.file_paths) > 0:
                log = ""
                with open(
                    self.file_paths[self.file_index], "r", encoding="utf-8"
                ) as file:
                    log = file.read()

                self.plot_data = self.viewModel.comprehensive_analysis(log)
                self.plot_canvas.plot_subplots(self.plot_data)
            else:
                ControlPanel.show_error_msg("未打开log文件")

    def set_analysis_intervel(self, intervel):
        self.viewModel.set_intervel(intervel)

    def loss_packet_analysis(self):

        if self.fun is None or self.fun != self.loss_packet_analysis:
            self.fun = self.loss_packet_analysis
            self.clear_container()

            # 做一个组件，让布局可以包含进去
            canvas_widget = QWidget(self)
            canvas_widget.setLayout(self.convas_gird)

            file_path = Path(self.file_paths[self.file_index])
            text_label = QLabel(self)
            text_label.setText(file_path.name + " 丢包变化量图")
            text_label.setStyleSheet("color: red;")
            self.container_layout.addWidget(text_label)

            self.plot_canvas = PlotCanvas(self, width=5, height=8)
            self.convas_gird.addWidget(self.plot_canvas, 0, 1)
            self.container_layout.addWidget(canvas_widget)

            # 添加文本框到容器
            text_label = QLabel(self)
            text_label.setText("错误提示")
            text_label.setStyleSheet("color: red;")
            self.container_layout.addWidget(text_label)

            self.text_edit = QTextEdit(self)

            self.text_edit.setReadOnly(True)

            # 创建滚动区域
            scroll_area = QScrollArea(self)
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(self.text_edit)

            self.container_layout.addWidget(scroll_area)

        if self.plot_canvas is not None:
            self.plot_canvas.clear(self.plot_data)
            log = ""
            if len(self.file_paths) > 0:
                with open(
                    self.file_paths[self.file_index], "r", encoding="utf-8"
                ) as file:
                    log = file.read()

                self.text_edit.setPlainText(self.viewModel.get_error_str(log))
                self.plot_data = self.viewModel.loss_packet_analysis(log)
                self.plot_canvas.plot_subplots(self.plot_data)
            else:
                ControlPanel.show_error_msg("未打开log文件")
                return

    def loss_packet_monitor(self):
        pass

    def show_previous_plot(self):
        file_cnt = len(self.file_paths) - 1

        if file_cnt >= self.file_index and self.file_index > 0:
            self.file_index -= 1
            self.fun()

    def show_next_plot(self):
        file_cnt = len(self.file_paths) - 1

        if file_cnt > self.file_index and self.file_index >= 0:
            self.file_index += 1
            self.fun()
