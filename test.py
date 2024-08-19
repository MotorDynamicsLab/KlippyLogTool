from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QCheckBox,
    QVBoxLayout,
    QWidget,
    QLabel,
)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("请选择你的兴趣爱好：", self)
        self.layout.addWidget(self.label)

        self.checkbox1 = QCheckBox("阅读", self)
        self.checkbox1.stateChanged.connect(self.update_label)
        self.layout.addWidget(self.checkbox1)

        self.checkbox2 = QCheckBox("旅行", self)
        self.checkbox2.stateChanged.connect(self.update_label)
        self.layout.addWidget(self.checkbox2)

        self.checkbox3 = QCheckBox("音乐", self)
        self.checkbox3.stateChanged.connect(self.update_label)
        self.layout.addWidget(self.checkbox3)

        self.checkbox4 = QCheckBox("运动", self)
        self.checkbox4.stateChanged.connect(self.update_label)
        self.layout.addWidget(self.checkbox4)

    def update_label(self):
        selected = []
        if self.checkbox1.isChecked():
            selected.append(self.checkbox1.text())
        if self.checkbox2.isChecked():
            selected.append(self.checkbox2.text())
        if self.checkbox3.isChecked():
            selected.append(self.checkbox3.text())
        if self.checkbox4.isChecked():
            selected.append(self.checkbox4.text())

        self.label.setText("你选择的兴趣爱好是：" + ", ".join(selected))


if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
