from concurrent.futures import ThreadPoolExecutor
import re
from collections import defaultdict
import numpy as np
from model.common import GlobalComm


class LogKlipper:
    def __init__(self, log) -> None:
        self.log = log

    def extract_newest_config(self):
        if self.log is not None and self.log != "":
            content = self.log
            end_index = content.rfind("=======================")
            if end_index != -1:
                start_index = content.rfind("===== Config file =====", 0, end_index)
                middle_content = content[
                    start_index + len("===== Config file =====") : end_index
                ].strip()
                return middle_content
        return GlobalComm.get_langdic_val("error_tip", "Err_CfgNotFoundError")

    def get_error_str(self):
        lines = self.log.split("\n")
        error_lines = [line for line in lines if "Got " in line]
        return "\n".join(error_lines)

    def get_stats_shucdown_info(self):
        start_str = r"Stats "
        end_str = r"Reactor garbage collection:"
        result = []
        reactor_start_index = reactor_end_index = 0

        while True:
            reactor_end_index = self.log.find(end_str, reactor_end_index)
            if reactor_end_index != -1:
                reactor_start_index = self.log.rfind(
                    start_str, reactor_start_index, reactor_end_index
                )
                result.append(self.log[reactor_start_index:reactor_end_index])
                reactor_start_index = reactor_end_index
                reactor_end_index += 100
            else:
                break

        return "\n######################\n".join(result)

    @staticmethod
    def save_to_file(cfg, save_path="out/klipper.cfg"):
        with open(save_path, "w") as file:
            file.write(cfg)


class LogStats:
    def __init__(self, log) -> None:
        self.log = log

    def __generate_stats_list(self):
        # 使用生成器表达式来节省内存
        self.stats_list = [
            line for line in self.log.splitlines() if line.startswith("Stats")
        ]

    def __parse_stats_key_info(self, stats_string):
        # 分割字符串
        parts = stats_string.split()

        # 初始化结果字典
        result = {}

        # 当前处理的模块名
        current_module = None

        for part in parts:
            if ":" in part:
                # 这是一个模块名或键值对
                if "=" not in part:
                    # 这是一个模块名
                    current_module = part.rstrip(":")
                    if current_module not in result:
                        result[current_module] = {}
                else:
                    # 这是一个键值对
                    key, value = part.split("=")
                    if current_module:
                        result[current_module][key] = value
                    else:
                        result[key] = value
            else:
                # 这是一个键值对
                if "=" in part:
                    key, value = part.split("=")
                    if current_module:
                        result[current_module][key] = value
                    else:
                        result[key] = value
                else:
                    pass
                    # 处理没有等号的部分
                    # print(f"Warning: Skipping invalid part '{part}'")

        return result

    def get_stats_info(self):
        self.__generate_stats_list()
        return "\n".join(self.stats_list)

    def get_stats_dicts(self):
        if hasattr(self, "_cached_stats_dicts"):
            return self._cached_stats_dicts

        self.__generate_stats_list()
        list_dict = []
        for stats_line in self.stats_list:
            list_dict.append(self.__parse_stats_key_info(stats_line))

        self._cached_stats_dicts = list_dict
        return list_dict

    def get_mcu_list(self, list_dicts):
        mcu = []
        list_dicts_cnt = len(list_dicts)
        if list_dicts_cnt != 0:
            dicts = list_dicts[list_dicts_cnt - 1]
            for module, data in dicts.items():
                if isinstance(data, dict):
                    for key, value in data.items():
                        if key == "mcu_awake":
                            mcu.append(module)
        return mcu

    def get_bytes_retransmit_incremental_list(self, interval, list_dicts):
        try:
            i = 0
            is_reset = False
            list_retransmit_mcus = []
            mcu_list = self.get_mcu_list(list_dicts)
            cur_val = {}
            max_val = {}
            min_val = {}
            for mcu in mcu_list:
                try:
                    if len(list_dicts) > 0:
                        dicts = list_dicts[0]
                        cur_val[mcu] = max_val[mcu] = min_val[mcu] = int(
                            dicts[mcu]["bytes_retransmit"]
                        )
                except Exception:
                    cur_val[mcu] = max_val[mcu] = min_val[mcu] = 0

            for dicts in list_dicts:
                for mcu in mcu_list:
                    if mcu in dicts:
                        try:
                            cur_val[mcu] = int(dicts[mcu]["bytes_retransmit"])
                        except Exception:
                            pass

                    if cur_val[mcu] < min_val[mcu]:
                        min_val[mcu] = cur_val[mcu]
                        is_reset = True

                    if cur_val[mcu] > max_val[mcu]:
                        max_val[mcu] = cur_val[mcu]

                i += 1
                if interval == i:
                    i = 0
                    temp_list = []
                    for mcu in mcu_list:
                        if is_reset:
                            temp_list.append(min_val[mcu] - max_val[mcu])
                        else:
                            temp_list.append(max_val[mcu] - min_val[mcu])

                        # debug
                        # if mcu == "nhk":
                        #     print(
                        #         mcu,
                        #         ":",
                        #         min_val[mcu],
                        #         max_val[mcu],
                        #         cur_val[mcu],
                        #         max_val[mcu] - min_val[mcu],
                        #     )
                        # Starting from the last result
                        max_val[mcu] = min_val[mcu] = cur_val[mcu]

                    is_reset = False
                    list_retransmit_mcus.append(temp_list)

            if len(list_dicts) % interval != 0:
                temp_list = []
                for mcu in mcu_list:
                    try:
                        temp_list.append(max_val[mcu] - min_val[mcu])
                    except Exception:
                        pass

                    # Starting from the last result
                    max_val[mcu] = min_val[mcu] = cur_val[mcu]
                list_retransmit_mcus.append(temp_list)

            # print(list_retransmit_mcus, len(list_retransmit))
            return list_retransmit_mcus, mcu_list

        except Exception as e:
            print("exception def get_bytes_retransmit_incremental_list: ", e)

    def get_target_temp_list(self, interval, list_dicts):
        try:
            extruder_temp_list = []
            bed_temp_list = []
            val_list = []

            for i, dicts in enumerate(list_dicts):
                if "heater_bed" in dicts and "extruder" in dicts:
                    val_list.append(
                        (
                            float(dicts["heater_bed"]["target"]),
                            float(dicts["heater_bed"]["temp"]),
                            float(dicts["extruder"]["target"]),
                            float(dicts["extruder"]["temp"]),
                        )
                    )

                if (i + 1) % interval == 0:
                    extruder_temp_list.append(
                        (
                            np.min([t[0] for t in val_list]),
                            np.min([t[1] for t in val_list]),
                        )
                    )
                    bed_temp_list.append(
                        (
                            np.min([t[2] for t in val_list]),
                            np.min([t[3] for t in val_list]),
                        )
                    )
                    val_list.clear()  # Clear the list for the next interval

            return (extruder_temp_list, bed_temp_list)

        except Exception as e:
            print("异常：", e)
