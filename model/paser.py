from model.common import GlobalComm, Utilities
from model.klipper_log import LogKlipper, LogStats
import pandas as pd


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
            {  # Common part
                "subplots": (2, 1, 1),
                "title": GlobalComm.get_langdic_val(
                    "analysis_plot_pic", "title_bytes_retransmit"
                ),
                "xlabel": GlobalComm.get_langdic_val(
                    "analysis_plot_pic", "xlabel_bytes_retransmit"
                ),
                "ylabel": GlobalComm.get_langdic_val(
                    "analysis_plot_pic", "ylabel_bytes_retransmit"
                ),
            },
            { # Specific graph data
                "x": x,
                "y": list_retransmit,
                "label": GlobalComm.get_langdic_val(
                    "analysis_plot_pic", "label_bytes_retransmit"
                ),
                "linestyle": "-",
                "color": "b",
            },
        ]
        return plot_data

    def analysis_extruder_temp(self):
        # Analyze text
        list_dicts = self.stats.get_stats_dicts()
        extruder_temp_list, _ = self.stats.get_target_temp_list(list_dicts)
        target_list = [t[0] for t in extruder_temp_list]
        temp_list = [t[1] for t in extruder_temp_list]

        target_extruder = pd.Series(target_list)
        temp_extruder = pd.Series(temp_list)

        target_extruder_mean = target_extruder.rolling(window=100).mean()
        temp_extruder_mean = temp_extruder.rolling(window=100).mean()

        # Generate graph data
        plot_data = [
            {  # Common part
                "subplots": (2, 2, 3),
                "title": GlobalComm.get_langdic_val(
                    "analysis_plot_pic", "title_extruder"
                ),
                "xlabel": GlobalComm.get_langdic_val(
                    "analysis_plot_pic", "xlabel_extruder"
                ),
                "ylabel": GlobalComm.get_langdic_val(
                    "analysis_plot_pic", "ylabel_extruder"
                ),
            },
            {  # Specific graph data
                "x": target_extruder_mean.index,
                "y": target_extruder_mean,
                "label": GlobalComm.get_langdic_val(
                    "analysis_plot_pic", "label_extruder_target"
                ),
                "color": "b",
                "linestyle": "--",
            },
            {
                "x": temp_extruder_mean.index,
                "y": temp_extruder_mean,
                "label": GlobalComm.get_langdic_val(
                    "analysis_plot_pic", "label_extruder"
                ),
                "color": "r",
                "linestyle": "-",
            },
        ]
        return plot_data

    def analysis_bed_temp(self):
        # Analyze text
        list_dicts = self.stats.get_stats_dicts()
        _, bed_temp_list = self.stats.get_target_temp_list(list_dicts)
        target_list = [t[0] for t in bed_temp_list]
        temp_list = [t[1] for t in bed_temp_list]

        target_bed = pd.Series(target_list)
        temp_bed = pd.Series(temp_list)

        target_bed_mean = target_bed.rolling(window=100).mean()
        temp_bed_mean = temp_bed.rolling(window=100).mean()

        # Generate graph data
        plot_data = [
            {  # Common part
                "subplots": (2, 2, 4),
                "title": GlobalComm.get_langdic_val("analysis_plot_pic", "title_bed"),
                "xlabel": GlobalComm.get_langdic_val("analysis_plot_pic", "xlabel_bed"),
                "ylabel": GlobalComm.get_langdic_val("analysis_plot_pic", "ylabel_bed"),
            },
            {  # Specific graph data
                "x": target_bed_mean.index,
                "y": target_bed_mean,
                "label": GlobalComm.get_langdic_val(
                    "analysis_plot_pic", "label_bed_target"
                ),
                "color": "b",
                "linestyle": "--",
            },
            {
                "x": temp_bed_mean.index,
                "y": temp_bed_mean,
                "label": GlobalComm.get_langdic_val("analysis_plot_pic", "label_bed"),
                "color": "r",
                "linestyle": "-",
            },
        ]
        return plot_data
