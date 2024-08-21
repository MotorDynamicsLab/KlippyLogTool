"""
@File    :   main_view.py
@Time    :   2024/08/20 23:27:25
@Desc    :   Describes the basic framework of the main interface, excluding the core display part
"""

import locale
import os
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMessageBox,
    QMainWindow,
    QAction,
    QInputDialog,
)

from model.common import GlobalComm, Utilities
from view.control_view import ControlPanel


class MainPanel(QMainWindow):
    def __init__(self):
        super().__init__()

        result = GlobalComm.load_json_cfg()
        if not result:
            MainPanel.exit_app()

        self.load_current_languag()

        # Main frame initialization
        self.setWindowTitle(GlobalComm.get_langdic_val("view", "title"))
        # self.showMaximized()
        self.resize(800, 800)

        self.menu_init()
        self.central_widget_init()

    def central_widget_init(self):
        self.central_widget = ControlPanel(self)
        self.setCentralWidget(self.central_widget)

    def menu_init(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu(GlobalComm.get_langdic_val("view", "file_menu"))

        # File menu #
        # Open the current log
        action = QAction(
            GlobalComm.get_langdic_val("view", "file_menu_klipper_log"), self
        )
        action.triggered.connect(self.open_log_file)
        file_menu.addAction(action)

        # Create and save configuration files
        action = QAction(
            GlobalComm.get_langdic_val("view", "file_menu_klipper_cfg"), self
        )
        action.triggered.connect(self.open_cfg_file)
        file_menu.addAction(action)

        # Open the current stats file
        action = QAction(
            GlobalComm.get_langdic_val("view", "file_menu_stats_log"), self
        )
        action.triggered.connect(self.open_stats_file)
        file_menu.addAction(action)

        # Check printed
        action = QAction(GlobalComm.get_langdic_val("view", "file_check_print"), self)
        action.triggered.connect(self.print_check)
        file_menu.addAction(action)

        # Exit application
        action = QAction(GlobalComm.get_langdic_val("view", "file_menu_exit"), self)
        action.triggered.connect(MainPanel.exit_app)
        file_menu.addAction(action)

        # Configuration menu #
        set_menu = menu_bar.addMenu(GlobalComm.get_langdic_val("view", "set_menu"))

        # Language conversion
        language_menu = set_menu.addMenu(
            GlobalComm.get_langdic_val("view", "set_menu_language")
        )
        self.english_action = QAction(
            GlobalComm.get_langdic_val("view", "set_menu_language_en"),
            self,
            checkable=True,
        )
        self.english_action.setChecked(self.language == "en")
        self.english_action.triggered.connect(self.set_language_en)
        language_menu.addAction(self.english_action)

        self.chinese_action = QAction(
            GlobalComm.get_langdic_val("view", "set_menu_language_ch"),
            self,
            checkable=True,
        )
        self.chinese_action.setChecked(self.language == "zh")
        self.chinese_action.triggered.connect(self.set_language_zh)
        language_menu.addAction(self.chinese_action)

        # Packet loss interval
        action = QAction(GlobalComm.get_langdic_val("view", "set_menu_loss_set"), self)
        action.triggered.connect(self.show_input_dialog)
        set_menu.addAction(action)

        # about #
        about_action = QAction(GlobalComm.get_langdic_val("view", "about"), self)
        about_action.triggered.connect(self.show_about_dialog)
        menu_bar.addAction(about_action)

    ### Function function
    def update_language_ui(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    def load_current_languag(self):
        if GlobalComm.setting_json["language"] == "":
            lang, _ = locale.getdefaultlocale()
            if lang and lang.startswith("zh"):
                self.language = "zh"
            elif lang and lang.startswith("en"):
                self.language = "en"
            else:
                self.language = "en"  # 若是其他语言默认中文

            GlobalComm.set_cur_language(self.language)
        else:
            self.language = GlobalComm.setting_json["language"]

    ### event
    def set_language_en(self):
        self.language = "en"
        self.chinese_action.setChecked(False)
        GlobalComm.save_json_setting(
            "language", self.language
        )  # Save the selected language
        self.update_language_ui()

    def set_language_zh(self):
        self.language = "zh"
        self.english_action.setChecked(False)
        GlobalComm.save_json_setting(
            "language", self.language
        )  # Save the selected language
        self.update_language_ui()

    def show_input_dialog(self):
        # Show an input dialog to get user input
        text, ok = QInputDialog.getText(
            self,
            GlobalComm.get_langdic_val("view", "dialog_input_title"),
            GlobalComm.get_langdic_val("view", "dialog_input_test"),
            text=GlobalComm.setting_json["loss_interval_set"],
        )

        if ok and text:
            self.central_widget.set_analysis_intervel(int(text))

    def show_about_dialog(self):
        about_text = GlobalComm.get_langdic_val("view", "about_text")
        QMessageBox.information(
            self,
            GlobalComm.get_langdic_val("view", "dialog_about_title"),
            about_text,
        )

    def print_check(self):
        counts = self.central_widget.get_print_cnt()
        result = ", ".join([f"'{target}': {count}" for target, count in counts.items()])
        print(result)
        QMessageBox.information(
            self,
            GlobalComm.get_langdic_val("view", "dialog_about_title"),
            result,
        )

    def open_log_file(self):
        Utilities.open_file_or_dir(self.central_widget.get_current_file_path())

    def open_stats_file(self):
        self.central_widget.save_some_files(True)
        Utilities.open_file_or_dir(GlobalComm.setting_json["stats_log"])

    def open_cfg_file(self):
        self.central_widget.save_some_files()
        Utilities.open_file_or_dir(GlobalComm.setting_json["klipper_cfg"])

    @staticmethod
    def exit_app():
        QApplication.quit()

    # Overload the closeEvent method
    def closeEvent(self, event):
        self.central_widget.stop_thread()  # Stop thread when closing window
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainPanel()
    main_window.show()
    sys.exit(app.exec_())
