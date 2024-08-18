from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QPushButton,
    QVBoxLayout,
    QTextEdit,
    QLabel,
    QSizePolicy,
    QFrame,
)
from PyQt5.QtGui import QMovie
from model.analysis_thread import AnalysisThread
from model.common import GlobalComm, Utilities
from model.control_model import ControlModel
from PyQt5.QtCore import QThread, pyqtSignal, Qt

from view.loading_view import LoadingPanel
from view.plot_canvas import PlotCanvas


class ControlPanel(QWidget):

    def __init__(self, parent=None):
        super(ControlPanel, self).__init__(parent)

        self.subplot_data = []
        self.file_paths = ["logs/klippy.log"]
        self.cur_file_path = ""
        self.log = ""

        self.loading_view = LoadingPanel(self)
        self.model = ControlModel()
        self.init_widget()

    ############################
    #  Interface related #
    ############################
    def init_widget(self):
        grid_layout = QGridLayout(self)
        self.setLayout(grid_layout)

        # first line
        open_log_btn = QPushButton(GlobalComm.get_langdic_val("view", "btn_open_log"))
        open_log_btn.clicked.connect(self.open_log)
        grid_layout.addWidget(open_log_btn, 0, 0, 1, 3)

        # Occupy three columns of a row Three buttons in the second row
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
        loss_packet_monitor_btn.setEnabled(False)

        # Place a qv box layout page container in the remaining position
        container = QWidget(self)
        self.container_layout = QVBoxLayout(container)
        grid_layout.addWidget(container, 2, 0, 1, 3)

        # Other data
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
        self.text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return self.text_edit

    def draw_cfg_main_info(self):
        self.cfg_main_edit = QTextEdit(self)
        self.cfg_main_edit.setReadOnly(True)
        self.cfg_main_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return self.cfg_main_edit

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
        self.plot_canvas = PlotCanvas(self, width=5, height=7)
        self.convas_gird = QGridLayout(canvas_widget)
        self.convas_gird.addWidget(button_prev, 0, 0)
        self.convas_gird.addWidget(self.plot_canvas, 0, 1)
        self.convas_gird.addWidget(button_next, 0, 2)
        return canvas_widget

    def init_loss_packet_view(self):
        self.file_path = Path(self.file_paths[self.file_index])
        if self.fun is None or self.fun != self.loss_packet_analysis:
            self.fun = self.loss_packet_analysis
            self.clear_container()

            # Packet loss graph
            self.file_title_label = self.draw_title_label(self.file_path.name)
            self.container_layout.addWidget(self.file_title_label)

            canvas_widget = self.draw_analytical_diagram()
            self.container_layout.addWidget(canvas_widget)

            # Error message
            title_label = self.draw_title_label(
                GlobalComm.get_langdic_val("analysis_plot_pic", "title_error_tip_label")
            )
            self.container_layout.addWidget(title_label)
            self.container_layout.addWidget(self.draw_error_tip())

            # Add main cfg information
            title_label = self.draw_title_label(
                GlobalComm.get_langdic_val("analysis_plot_pic", "title_cfg_tip_label")
            )
            self.container_layout.addWidget(title_label)
            cfg_main_edit = self.draw_cfg_main_info()
            self.container_layout.addWidget(cfg_main_edit)

        self.loading_view.init_loading_QFrame()

    def init_comprehensive_view(self):
        # Clear previous display
        if self.fun is None or self.fun != self.comprehensive_analysis:
            self.fun = self.comprehensive_analysis
            self.clear_container()

            # Add analysis chart
            canvas_widget = self.draw_analytical_diagram()
            self.container_layout.addWidget(canvas_widget)

        self.loading_view.init_loading_QFrame()

    ############################
    ## Function function
    ############################
    def clear_container(self):
        for i in reversed(range(self.container_layout.count())):
            widget = self.container_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def save_some_files(self, only_cfg=False):
        self.model.save_files(self.file_paths[self.file_index], only_cfg)

    def set_analysis_intervel(self, intervel):
        self.model.set_intervel(intervel)

    def update_cur_log(self):
        if len(self.file_paths) > 0:
            log = self.model.update_current_log(
                self.cur_file_path, self.file_paths[self.file_index]
            )

            if log != "":
                self.cur_file_path = self.file_paths[self.file_index]
                self.log = log

    #############################
    # event handling #
    ############################
    def open_log(self):
        file_paths = Utilities.get_file_paths(self)
        if len(file_paths) != 0:
            self.file_paths = file_paths
            self.file_index = 0

    def comprehensive_analysis(self):
        try:
            # init display
            self.init_comprehensive_view()
            self.loading_view.run_loading_git()

            # parse log
            if self.plot_canvas is not None:
                self.plot_canvas.clear(self.subplot_data)
                self.update_cur_log()

                # Create and start analysis thread
                analysis_thread = AnalysisThread(
                    self.log, self.model, Utilities.get_current_function_name()
                )
                analysis_thread.bind_event(
                    self.on_analysis_complete, self.on_error_occurred
                )
                analysis_thread.start()
        except Exception as e:
            error = f"comprehensive_analysis exceptions: {e}"
            Utilities.show_error_msg(error)

    def loss_packet_analysis(self):
        try:
            # init display
            self.init_loss_packet_view()
            self.loading_view.run_loading_git()

            # parse log
            if self.plot_canvas is not None:
                self.plot_canvas.clear(self.subplot_data)
                self.file_update = self.update_cur_log() != ""

                # todo 这部分的页面更新清理掉到别处
                self.file_title_label.setText(self.file_path.name)
                self.cfg_main_edit.setPlainText(
                    self.model.output_main_cfg_info(self.log, self.file_update)
                )
                self.text_edit.setPlainText(self.model.get_error_str(self.log))

                # Create and start analysis thread
                analysis_thread = AnalysisThread(
                    self.log, self.model, Utilities.get_current_function_name()
                )
                analysis_thread.bind_event(
                    self.on_analysis_complete, self.on_error_occurred
                )
                analysis_thread.start()

        except Exception as e:
            error = f"exceptions: {e}"  # todo, 显示错乱当报异常时
            Utilities.show_error_msg(error)

    def on_analysis_complete(self, result, task_type):
        if task_type == "comprehensive_analysis":
            pass
        elif task_type == "loss_packet_analysis":
            pass
        self.subplot_data = result
        self.plot_canvas.plot_subplots(self.subplot_data)
        self.loading_view.stop_loading_gif()

    def on_error_occurred(self, error):
        Utilities.show_error_msg(f"分析错误: {error}")
        self.loading_view.stop_loading_gif()

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
