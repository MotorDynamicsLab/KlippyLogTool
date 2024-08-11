import sys
import json
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QAction,
    QMessageBox,
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QMenuBar,
)
from PyQt5.QtCore import Qt

# Constants for languages
LANGUAGES = {
    "en": {
        "title": "Input Dialog Example",
        "file_menu": "File",
        "open": "Open",
        "exit": "Exit",
        "edit_menu": "Edit",
        "sub_menu": "More Options",
        "sub_sub_menu": "Sub Options",
        "input_prompt": "Enter a numeric value:",
        "input_received": "Input Received",
        "input_warning": "Please enter a valid numeric value.",
        "about": "About",
        "about_text": "This is an example application to demonstrate language switching and input dialogs.",
    },
    "zh": {
        "title": "输入对话框示例",
        "file_menu": "文件",
        "open": "打开",
        "exit": "退出",
        "edit_menu": "编辑",
        "sub_menu": "更多选项",
        "sub_sub_menu": "子选项",
        "input_prompt": "输入一个数字值:",
        "input_received": "输入已接收",
        "input_warning": "请输入有效的数字值。",
        "about": "关于",
        "about_text": "这是一个示例应用程序，用于演示语言切换和输入对话框。",
    },
}


# Function to load language from a JSON file
def load_language():
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
            return settings.get("language", "en")  # Default to English
    except FileNotFoundError:
        return "en"  # Default to English


# Function to save language to a JSON file
def save_language(lang):
    with open("settings.json", "w") as f:
        json.dump({"language": lang}, f)


class InputDialog(QDialog):
    def __init__(self, parent=None, language="en"):
        super().__init__(parent)
        self.setWindowTitle(LANGUAGES[language]["input_prompt"])

        # Create a layout
        layout = QVBoxLayout(self)

        # Create a QLineEdit with a double validator
        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText(LANGUAGES[language]["input_prompt"])
        layout.addWidget(self.line_edit)

        # Create OK and Cancel buttons
        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.accept)  # Accept the dialog
        layout.addWidget(ok_button)

        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.reject)  # Reject the dialog
        layout.addWidget(cancel_button)

    def get_value(self):
        return self.line_edit.text()  # Return the text from the QLineEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.language = load_language()  # Load the language setting
        self.setWindowTitle(LANGUAGES[self.language]["title"])
        self.setGeometry(100, 100, 400, 300)

        # Create a menu bar
        menu_bar = self.menuBar()

        # Create a language menu
        language_menu = menu_bar.addMenu("Language")

        # Add language options
        english_action = QAction("English", self, checkable=True)
        english_action.setChecked(self.language == "en")
        english_action.triggered.connect(self.set_language_en)
        language_menu.addAction(english_action)

        chinese_action = QAction("Chinese", self, checkable=True)
        chinese_action.setChecked(self.language == "zh")
        chinese_action.triggered.connect(self.set_language_zh)
        language_menu.addAction(chinese_action)

        # Create a file menu
        self.file_menu = menu_bar.addMenu(LANGUAGES[self.language]["file_menu"])

        # Create an action with no submenus
        open_action = QAction(LANGUAGES[self.language]["open"], self)
        open_action.triggered.connect(self.show_input_dialog)
        self.file_menu.addAction(open_action)

        # Create another action with no submenus
        exit_action = QAction(LANGUAGES[self.language]["exit"], self)
        exit_action.triggered.connect(self.close)  # Close the application
        self.file_menu.addAction(exit_action)

        # Create an edit menu with submenus
        edit_menu = menu_bar.addMenu(LANGUAGES[self.language]["edit_menu"])

        # Submenu
        more_options_menu = edit_menu.addMenu(LANGUAGES[self.language]["sub_menu"])

        # Sub-submenu
        sub_options_menu = more_options_menu.addMenu(
            LANGUAGES[self.language]["sub_sub_menu"]
        )
        sub_option1 = QAction("Sub Option 1", self)
        sub_option2 = QAction("Sub Option 2", self)
        sub_options_menu.addAction(sub_option1)
        sub_options_menu.addAction(sub_option2)

        # Create an About menu item
        about_action = QAction(LANGUAGES[self.language]["about"], self)
        about_action.triggered.connect(self.show_about_dialog)
        menu_bar.addAction(about_action)

    def show_input_dialog(self):
        dialog = InputDialog(self, self.language)
        if dialog.exec_() == QDialog.Accepted:  # Check if OK was clicked
            text = dialog.get_value()
            if text:  # Ensure there's input
                try:
                    value = float(text)
                    self.process_input(value)
                except ValueError:
                    QMessageBox.warning(
                        self,
                        LANGUAGES[self.language]["input_received"],
                        LANGUAGES[self.language]["input_warning"],
                    )

    def process_input(self, value):
        QMessageBox.information(
            self, LANGUAGES[self.language]["input_received"], f"You entered: {value}"
        )

    def show_about_dialog(self):
        QMessageBox.information(
            self,
            LANGUAGES[self.language]["about"],
            LANGUAGES[self.language]["about_text"],
        )

    def set_language_en(self):
        self.language = "en"
        save_language(self.language)  # Save the selected language
        self.update_ui()

    def set_language_zh(self):
        self.language = "zh"
        save_language(self.language)  # Save the selected language
        self.update_ui()

    def update_ui(self):
        self.setWindowTitle(LANGUAGES[self.language]["title"])
        self.file_menu.setTitle(LANGUAGES[self.language]["file_menu"])
        self.file_menu.actions()[0].setText(LANGUAGES[self.language]["open"])
        self.file_menu.actions()[1].setText(LANGUAGES[self.language]["exit"])
        # Update edit menu
        self.menuBar().actions()[1].setText(LANGUAGES[self.language]["edit_menu"])
        self.menuBar().actions()[1].menu().setTitle(
            LANGUAGES[self.language]["edit_menu"]
        )


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
