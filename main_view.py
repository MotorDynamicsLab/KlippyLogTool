import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QMessageBox,
    QMainWindow,
    QAction,
    QInputDialog,
)

from model.common import GlobalComm, Utilities
from view.control_view import ControlPanel


class MainPanel(QMainWindow):
    ### 界面初始化
    def __init__(self):
        super().__init__()

        GlobalComm.load_json_cfg()
        self.language = GlobalComm.setting_json["language"]

        # 主框架初始化
        self.setWindowTitle(GlobalComm.get_langdic_val("view", "title"))
        # self.showMaximized()
        self.resize(800, 800)

        self.menu_init()
        self.central_widget_init()

    def central_widget_init(self):
        self.central_widget = ControlPanel(self)
        self.setCentralWidget(self.central_widget)

    def menu_init(self):
        self.menu_bar = self.menuBar()
        file_menu = self.menu_bar.addMenu(
            GlobalComm.get_langdic_val("view", "file_menu")
        )

        # 文件菜单 #
        action = QAction(
            GlobalComm.get_langdic_val("view", "file_menu_mid_result"), self
        )
        action.triggered.connect(self.save_result)
        file_menu.addAction(action)

        # 创建保存配置文件
        action = QAction(
            GlobalComm.get_langdic_val("view", "file_menu_klipper_cfg"), self
        )
        action.triggered.connect(self.open_cfg_file)
        file_menu.addAction(action)

        # 退出应用
        action = QAction(GlobalComm.get_langdic_val("view", "file_menu_exit"), self)
        action.triggered.connect(self.exit_app)
        file_menu.addAction(action)

        # 配置菜单 #
        set_menu = self.menu_bar.addMenu(GlobalComm.get_langdic_val("view", "set_menu"))

        # 语言转换
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

        # 丢包间隔
        action = QAction(GlobalComm.get_langdic_val("view", "set_menu_loss_set"), self)
        action.triggered.connect(self.show_input_dialog)
        set_menu.addAction(action)

        # 关于 #
        about_action = QAction(GlobalComm.get_langdic_val("view", "about"), self)
        about_action.triggered.connect(self.show_about_dialog)
        self.menu_bar.addAction(about_action)

    ### 功能函数
    def update_language_ui(self):
        # todo, 重启软件，加载语言最新
        pass

    ### 事件
    def set_language_en(self):
        self.language = "en"
        self.chinese_action.setChecked(False)
        GlobalComm.save_language(self.language)  # Save the selected language
        self.update_language_ui()

    def set_language_zh(self):
        self.language = "zh"
        self.english_action.setChecked(False)
        GlobalComm.save_language(self.language)  # Save the selected language
        self.update_language_ui()

    def show_input_dialog(self):
        # Show an input dialog to get user input
        text, ok = QInputDialog.getText(
            self,
            GlobalComm.get_langdic_val("view", "dialog_input_title"),
            GlobalComm.get_langdic_val("view", "dialog_input_test"),
        )

        if ok and text:
            self.central_widget.set_analysis_intervel(int(text))

    def show_about_dialog(self):
        about_text = GlobalComm.get_langdic_val(
            "view", "dialog_about_title"
        )  # todo, 进一步处理关于信息
        QMessageBox.information(
            self,
            GlobalComm.get_langdic_val("view", "dialog_about_title"),
            about_text,
        )

    def save_result(self):
        self.central_widget.save_some_files(True)
        Utilities.open_file_or_dir(GlobalComm.setting_json["ref_file_dir"]["dir_out"])

    def open_cfg_file(self):
        self.central_widget.save_some_files()
        Utilities.open_file_or_dir(
            GlobalComm.setting_json["ref_file_dir"]["klipper_cfg"]
        )

    def exit_app(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainPanel()
    main_window.show()
    sys.exit(app.exec_())
