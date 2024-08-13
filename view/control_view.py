from pathlib import Path
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

from model.common import GlobalComm, Utilities
from model.control_view_model import ControlViewModel
import matplotlib.font_manager as fm


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        font_path = "C:/Windows/Fonts/simhei.ttf"  # todo,放置到文件中读取
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.prop = fm.FontProperties(fname=font_path)
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
        ax.set_title(data["title"], fontproperties=self.prop)
        ax.set_xlabel(data["xlabel"], fontproperties=self.prop)
        ax.set_ylabel(data["ylabel"], fontproperties=self.prop)
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
                ax.legend(loc="upper right", prop=self.prop)
                self.axes.append(ax)

        cursor = mplcursors.cursor(self.axes, hover=True)

        @cursor.connect("add")
        def on_add(sel):
            x, y = sel.target
            line = sel.artist
            label = line.get_label()
            sel.annotation.set_text(f"{label}\nX: {x}\nY: {y}")
            sel.annotation.set_fontproperties(self.prop)

        self.draw()


class ControlPanel(QWidget):

    def __init__(self, parent=None):
        super(ControlPanel, self).__init__(parent)

        self.plot_data = []
        self.file_paths = ["logs/klippy.log"]

        self.viewModel = ControlViewModel()
        self.init_widget()

    def init_widget(self):
        grid_layout = QGridLayout(self)
        self.setLayout(grid_layout)

        # 第一行
        open_log_btn = QPushButton(GlobalComm.get_langdic_val("view", "btn_open_log"))
        open_log_btn.clicked.connect(self.open_log)
        grid_layout.addWidget(open_log_btn, 0, 0, 1, 3)  # 占用一行的三列

        # 第二行三个按钮
        comprehensive_analysis_btn = QPushButton(
            GlobalComm.get_langdic_val("view", "btn_comprehensive_analysis")
        )
        comprehensive_analysis_btn.clicked.connect(self.comprehensive_analysis)
        grid_layout.addWidget(comprehensive_analysis_btn, 1, 0)

        loss_packet_analysis_btn = QPushButton(
            GlobalComm.get_langdic_val("view", "btn_loss_packet_analysis")
        )
        loss_packet_analysis_btn.clicked.connect(self.loss_packet_analysis)
        grid_layout.addWidget(loss_packet_analysis_btn, 1, 1)

        loss_packet_monitor_btn = QPushButton(
            GlobalComm.get_langdic_val("view", "btn_loss_packet_monitor")
        )
        loss_packet_monitor_btn.clicked.connect(self.loss_packet_monitor)
        grid_layout.addWidget(loss_packet_monitor_btn, 1, 2)

        # 剩下的位置放一个QVBoxLayout布局的页面容器
        container = QWidget(self)
        self.container_layout = QVBoxLayout(container)
        grid_layout.addWidget(container, 2, 0, 1, 3)

        # 其他数据
        self.file_index = 0
        self.fun = None

    def draw_title_label(self, title_str):
        text_label = QLabel(self)
        text_label.setText(title_str)
        text_label.setStyleSheet("color: red;")
        return text_label

    def draw_error_tip(self):
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        # 创建滚动区域
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.text_edit)
        return scroll_area

    def draw_analytical_diagram(self):
        # Button for switching left and right of the image
        button_prev = QPushButton("<")
        button_next = QPushButton(">")
        button_prev.setFixedSize(30, 30)
        button_next.setFixedSize(30, 30)
        button_prev.clicked.connect(self.show_previous_plot)
        button_next.clicked.connect(self.show_next_plot)

        # Draw a graph showing the results
        canvas_widget = QWidget(self)
        self.plot_canvas = PlotCanvas(self, width=5, height=8)
        self.convas_gird = QGridLayout(canvas_widget)
        self.convas_gird.addWidget(button_prev, 0, 0)
        self.convas_gird.addWidget(self.plot_canvas, 0, 1)
        self.convas_gird.addWidget(button_next, 0, 2)
        return canvas_widget

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

    def set_analysis_intervel(self, intervel):
        self.viewModel.set_intervel(intervel)

    # 事件处理
    def open_log(self):
        self.file_paths = Utilities.get_file_paths(self)
        self.file_index = 0

    def comprehensive_analysis(self):
        if self.fun is None or self.fun != self.comprehensive_analysis:
            self.fun = self.comprehensive_analysis
            self.clear_container()
            canvas_widget = self.draw_analytical_diagram()
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
                ControlPanel.show_error_msg(
                    GlobalComm.get_langdic_val("error_tip", "Err_NotOpenLog")
                )

    def loss_packet_analysis(self):
        if self.fun is None or self.fun != self.loss_packet_analysis:
            self.fun = self.loss_packet_analysis
            self.clear_container()

            # 丢包图
            file_path = Path(self.file_paths[self.file_index])
            title_label = self.draw_title_label(file_path.name)
            self.container_layout.addWidget(title_label)

            canvas_widget = self.draw_analytical_diagram()
            self.container_layout.addWidget(canvas_widget)

            # 错误提示
            title_label = self.draw_title_label(
                GlobalComm.get_langdic_val("analysis_plot_pic", "title_error_tip_label")
            )
            self.container_layout.addWidget(title_label)

            scroll_area = self.draw_error_tip()
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
                GlobalComm.get_langdic_val("error_tip", "Err_NotOpenLog")

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
