import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from paser_log.paser_log import LogKlipper, LogStats
import pandas as pd
import subprocess
import sys


class Utilities:
    @staticmethod
    def get_file_paths(parent):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        files, _ = QFileDialog.getOpenFileNames(
            parent,
            "Select File",
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


class PaserLog:
    def __init__(self, log):
        self.cfg = LogKlipper(log)
        self.stats = LogStats(log)

    # 产生解析报告
    def paser_cfg(self):
        cfg_str = self.cfg.extract_newest_config()
        Utilities.save_to_file(cfg_str, save_path="out/klipper.cfg")
        return cfg_str

    def paser_shucdown_info(self):
        stats_str = self.cfg.get_stats_shucdown_info()
        Utilities.save_to_file(stats_str, save_path="out/shucdown_info.txt")
        return stats_str

    def paser_error(self):
        error_str = self.cfg.get_error_str()
        Utilities.save_to_file(error_str, save_path="out/error.txt")
        return error_str

    def paser_stats(self):
        stats_str = self.stats.get_stats_info()
        Utilities.save_to_file(stats_str, save_path="out/stats.txt")
        return stats_str

    # 分析并产生图表
    def analysis_bytes_retransmit(self, intervel):
        # 分析文本
        list_dicts = self.stats.get_stats_dicts()
        list_retransmit = self.stats.get_bytes_retransmit_incremental_list(
            intervel, list_dicts
        )

        # 产生图数据
        x = list(range(len(list_retransmit)))
        plot_data = [
            {
                "subplots": (2, 1, 1),
                "title": "bytes retransmit magnitude of change",
                "xlabel": "stats intervals",
                "ylabel": "value of change",
            },
            {
                "x": x,
                "y": list_retransmit,
                "label": "value of change",
                "linestyle": "-",
                "color": "b",
            },
        ]
        return plot_data

    def analysis_extruder_temp(self):
        # 分析文本
        list_dicts = self.stats.get_stats_dicts()
        extruder_temp_list, _ = self.stats.get_target_temp_list(list_dicts)
        target_list = [t[0] for t in extruder_temp_list]
        temp_list = [t[1] for t in extruder_temp_list]

        target_extruder = pd.Series(target_list)
        temp_extruder = pd.Series(temp_list)

        target_extruder_mean = target_extruder.rolling(window=100).mean()
        temp_extruder_mean = temp_extruder.rolling(window=100).mean()

        # 产生图数据
        plot_data = [
            {  # 通用部分
                "subplots": (2, 2, 3),
                "title": "extruder temp",
                "xlabel": "stats intervals",
                "ylabel": "temp",
            },
            {
                "x": target_extruder_mean.index,
                "y": target_extruder_mean,
                "label": "target",
                "color": "b",
                "linestyle": "--",
            },
            {
                "x": temp_extruder_mean.index,
                "y": temp_extruder_mean,
                "label": "temp",
                "color": "r",
                "linestyle": "-",
            },
        ]
        return plot_data

    def analysis_bed_temp(self):
        # 分析文本
        list_dicts = self.stats.get_stats_dicts()
        _, bed_temp_list = self.stats.get_target_temp_list(list_dicts)
        target_list = [t[0] for t in bed_temp_list]
        temp_list = [t[1] for t in bed_temp_list]

        target_bed = pd.Series(target_list)
        temp_bed = pd.Series(temp_list)

        target_bed_mean = target_bed.rolling(window=100).mean()
        temp_bed_mean = temp_bed.rolling(window=100).mean()

        # 产生图数据
        plot_data = [
            {
                "subplots": (2, 2, 4),
                "title": "bed temp",
                "xlabel": "stats intervals",
                "ylabel": "temp",
            },
            {
                "x": target_bed_mean.index,
                "y": target_bed_mean,
                "label": "target",
                "color": "b",
                "linestyle": "--",
            },
            {
                "x": temp_bed_mean.index,
                "y": temp_bed_mean,
                "label": "temp",
                "color": "r",
                "linestyle": "-",
            },
        ]
        return plot_data


class MainViewModel:
    def __init__(self):
        pass

    def get_error_str(self, log):
        self.paser = PaserLog(log)
        return self.paser.paser_error()

    def output_analysis_result(self, log):
        if log != "":
            self.paser = PaserLog(log)
            self.paser.paser_cfg()
            self.paser.paser_stats()
            self.paser.paser_error()
            self.paser.paser_shucdown_info()

    def output_cfg(self, log):
        if log != "":
            self.paser.paser_cfg()

    def comprehensive_analysis(self, log):
        subplot_data = []
        if log != "":
            paser = PaserLog(log)
            subplot_data.append(paser.analysis_bytes_retransmit(100))
            subplot_data.append(paser.analysis_bed_temp())
            subplot_data.append(paser.analysis_extruder_temp())

        return subplot_data

    def loss_packet_analysis(self, log):
        subplot_data = []
        if log != "":
            paser = PaserLog(log)
            subplot_data.append(paser.analysis_bytes_retransmit(100))
        return subplot_data
