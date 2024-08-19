import random
from model.common import GlobalComm, RandomColor, Utilities
from model.klipper_log import LogKlipper, LogStats
import pandas as pd


class PaserLog:
    def __init__(self, log):
        self.cfg = LogKlipper(log)
        self.stats = LogStats(log)

    # Generate analysis report
    def paser_cfg(self):
        cfg_str = self.cfg.extract_newest_config()
        Utilities.save_to_file(cfg_str, save_path="out/klipper.cfg")
        return cfg_str

    def paser_cfg_info(self):
        return self.cfg.extract_newest_config()

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

    def paser_mcu(self):
        list_dicts = self.stats.get_stats_dicts()
        return self.stats.get_mcu_list(list_dicts)

    # Analyze and generate charts
    def analysis_bytes_retransmit(self, intervel):
        # todo 分析文本 , 以mcu分离多个变化线
        list_dicts = self.stats.get_stats_dicts()
        list_retransmit, mcu_list = self.stats.get_bytes_retransmit_incremental_list(
            intervel, list_dicts
        )

        loss_str = (
            GlobalComm.get_langdic_val("analysis_plot_pic", "title_bytes_retransmit")
            + "("
            + str(intervel)
            + ")"
        )
        # 产生图数据
        plot_data = [
            {  # Common part
                "subplots": (2, 1, 1),
                "title": loss_str,
                "xlabel": GlobalComm.get_langdic_val(
                    "analysis_plot_pic", "xlabel_bytes_retransmit"
                ),
                "ylabel": GlobalComm.get_langdic_val(
                    "analysis_plot_pic", "ylabel_bytes_retransmit"
                ),
            },
        ]

        i = 0
        color = RandomColor()
        for mcu in mcu_list:
            list_mcu = [sublist[i] for sublist in list_retransmit]
            i += 1
            plot_data.append(
                {  # Specific graph data
                    "x": list(range(len(list_retransmit))),
                    "y": list_mcu,
                    "label": mcu,
                    "linestyle": "-",
                    "color": color.random_color(),
                }
            )

        return plot_data

    def analysis_extruder_temp(self, intervel):
        # Analyze text
        list_dicts = self.stats.get_stats_dicts()
        extruder_temp_list, _ = self.stats.get_target_temp_list(intervel, list_dicts)
        target_list = [t[0] for t in extruder_temp_list]
        temp_list = [t[1] for t in extruder_temp_list]

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
                "x": list(range(len(target_list))),
                "y": target_list,
                "label": GlobalComm.get_langdic_val(
                    "analysis_plot_pic", "label_extruder_target"
                ),
                "color": "b",
                "linestyle": "--",
            },
            {
                "x": list(range(len(temp_list))),
                "y": temp_list,
                "label": GlobalComm.get_langdic_val(
                    "analysis_plot_pic", "label_extruder"
                ),
                "color": "r",
                "linestyle": "-",
            },
        ]
        return plot_data

    def analysis_bed_temp(self, intervel):
        # Analyze text
        list_dicts = self.stats.get_stats_dicts()
        _, bed_temp_list = self.stats.get_target_temp_list(intervel, list_dicts)
        target_list = [t[0] for t in bed_temp_list]
        temp_list = [t[1] for t in bed_temp_list]

        # Generate graph data
        plot_data = [
            {  # Common part
                "subplots": (2, 2, 4),
                "title": GlobalComm.get_langdic_val("analysis_plot_pic", "title_bed"),
                "xlabel": GlobalComm.get_langdic_val("analysis_plot_pic", "xlabel_bed"),
                "ylabel": GlobalComm.get_langdic_val("analysis_plot_pic", "ylabel_bed"),
            },
            {  # Specific graph data
                "x": list(range(len(target_list))),
                "y": target_list,
                "label": GlobalComm.get_langdic_val(
                    "analysis_plot_pic", "label_bed_target"
                ),
                "color": "b",
                "linestyle": "--",
            },
            {
                "x": list(range(len(temp_list))),
                "y": temp_list,
                "label": GlobalComm.get_langdic_val("analysis_plot_pic", "label_bed"),
                "color": "r",
                "linestyle": "-",
            },
        ]
        return plot_data
