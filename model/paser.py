import random
from model.common import GlobalComm, Utilities
from model.klipper_log import LogKlipper, LogStats
import pandas as pd


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


class PaserLog:
    def __init__(self, log):
        self.cfg = LogKlipper(log)
        self.stats = LogStats(log)

    # Generate analysis report
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
            + GlobalComm.setting_json["loss_interval_set"]
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
