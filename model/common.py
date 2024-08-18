import json
import random
from PyQt5.QtWidgets import (
    QFileDialog,
    QMessageBox,
)
import subprocess
import sys
import inspect


class RandomColor:
    def __init__(self):
        self.used_hues = []
        self.hue_step = 30  # 每次生成颜色之间的最小色调差异

    def random_color(self):
        while True:
            # 生成随机的 HSL 颜色
            h = random.randint(0, 360)
            s = 100
            l = 50

            # 检查颜色的色调是否已经被使用过
            if all(abs(h - used_hue) >= self.hue_step for used_hue in self.used_hues):
                self.used_hues.append(h)
                return self.hsl_to_rgb(h, s, l)

    def hsl_to_rgb(self, h, s, l):
        # h, s, l 都在 [0, 100] 范围内
        s /= 100
        l /= 100
        c = (1 - abs(2 * l - 1)) * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = l - c / 2

        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x

        r = (r + m) * 255
        g = (g + m) * 255
        b = (b + m) * 255

        return (r / 255, g / 255, b / 255)


class GlobalComm:
    language_json = dict()
    setting_json = dict()

    language = ""

    @staticmethod
    def get_langdic_val(sub_key_str, obj_str):
        return GlobalComm.language_json[GlobalComm.language][sub_key_str][obj_str]

    @staticmethod
    #!!! todo, throws an inevitable exception if the configuration file does not exist
    def load_json_cfg():
        try:
            with open("cfg/settings.json", "r", encoding="utf-8") as f:
                GlobalComm.setting_json = json.load(f)

            with open("cfg/language.json", "r", encoding="utf-8") as f:
                GlobalComm.language_json = json.load(f)
                GlobalComm.language = GlobalComm.setting_json["language"]

        except FileNotFoundError:
            return "global json is not exist"  # Default to English
        except Exception as e:
            print(f"其他错误: {e}")

    @staticmethod
    def set_cur_language(language):
        GlobalComm.language = language

    @staticmethod
    def save_json_setting(key, val):
        with open(GlobalComm.setting_json["cfg_setting"], "w") as f:
            GlobalComm.setting_json[key] = val
            json.dump(GlobalComm.setting_json, f, ensure_ascii=False, indent=4)


class Utilities:
    @staticmethod
    def get_file_paths(parent):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        files, _ = QFileDialog.getOpenFileNames(
            parent,
            GlobalComm.get_langdic_val("view", "dialog_open_file"),
            "",
            "All Files (*);;Text Files (*.log)",
            options=options,
        )

        return files

    @staticmethod
    def save_to_file(cfg, save_path):
        with open(save_path, "w") as file:
            file.write(cfg)

    @staticmethod
    def open_file_or_dir(path):
        if sys.platform.startswith("win"):
            # Windows
            subprocess.Popen(["start", "", path], shell=True)
        elif sys.platform.startswith("darwin"):
            # macOS
            subprocess.Popen(["open", path])
        else:
            # Linux
            subprocess.Popen(["xdg-open", path])

    @staticmethod
    def show_error_msg(error):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    @staticmethod
    def get_current_function_name():
        stack = inspect.stack()
        return stack[1].function
