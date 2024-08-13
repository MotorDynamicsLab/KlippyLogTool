import json
from PyQt5.QtWidgets import QFileDialog
import subprocess
import sys


class GlobalComm:
    language_json = dict()
    setting_json = dict()

    language = ""

    @staticmethod
    def get_langdic_val(sub_key_str, obj_str):
        return GlobalComm.language_json[GlobalComm.language][sub_key_str][obj_str]

    @staticmethod
    # todo, 抛出一个必然的异常，若配置文件不存在
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
    def save_language(language):
        with open(GlobalComm.setting_json["ref_file_dir"]["cfg_setting"], "w") as f:
            json.dump({"language": language}, f)


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
