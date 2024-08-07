import re
from collections import defaultdict


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
        return "警告: 未找到配置"  # todo，错误信息统一由类返回

    def get_errors(self):
        pattern = pattern = (
            r"(Reactor garbage collection:.*?Dumping send queue 100 messages)"
        )

        matches = re.findall(pattern, self.log, re.DOTALL)
        matches = [match.strip() + "\n" for match in matches]
        result_string = "\n".join(matches)
        return result_string

    @staticmethod
    def save_to_file(cfg, save_path="out/klipper.cfg"):
        with open(save_path, "w") as file:
            file.write(cfg)


class LogTemp:
    def __init__(self, log) -> None:
        self.log = log

    def __get_temp_info(self, target_str):
        start_index = self.log.rfind(target_str) + len(target_str)
        if start_index != -1:
            end_index = self.log.find("\n", start_index)
            target_temp = self.log[start_index:end_index].strip()
            return target_temp
        return None

    def get_newest_temp_target_dict(self):
        temp_dict = {}
        target_str = "Heater heater_bed approaching new target of "
        temp_dict["heater_bed_target"] = self.__get_temp_info(target_str)

        target_str = "Heater extruder approaching new target of "
        temp_dict["extruder_target"] = self.__get_temp_info(target_str)
        return temp_dict


class LogStats:
    def __init__(self, file_path) -> None:
        self.file_path = file_path

    def __generate_stats_list(self):
        self.stats_list = []
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                for line in file:
                    if line.startswith("Stats"):
                        self.stats_list.append(line.strip())
        except FileNotFoundError:
            return "错误: 文件未找到"

    def __parse_stats_key_info(self, stats_string):
        out_dicts = {}

        heater_bed_match = re.search(
            r"heater_bed:\s*target=(\d+)\s*temp=([\d.]+)", stats_string
        )
        if heater_bed_match:
            target = heater_bed_match.group(1)
            temp = heater_bed_match.group(2)
            out_dicts["heater_bed"] = {"target": target, "temp": temp}
        else:
            out_dicts["heater_bed"] = {"target": 0, "temp": 0}

        extruder_match = re.search(
            r"extruder:\s*target=(\d+)\s*temp=([\d.]+)", stats_string
        )
        if extruder_match:
            target = extruder_match.group(1)
            temp = extruder_match.group(2)
            out_dicts["extruder"] = {"target": target, "temp": temp}
        else:
            out_dicts["extruder"] = {"target": 0, "temp": 0}

        bytes_retransmit_matches = re.findall(r"bytes_retransmit=(\d+)", stats_string)
        if bytes_retransmit_matches:
            bytes_retransmit_list = [int(value) for value in bytes_retransmit_matches]
            out_dicts["bytes_retransmit"] = bytes_retransmit_list[0]
        else:
            out_dicts["bytes_retransmit"] = 0

        return out_dicts

    def get_stats_info(self):
        self.__generate_stats_list()
        return "\n".join(self.stats_list)

    def get_stats_dicts(self):
        self.__generate_stats_list()

        list_dict = []
        for stats_line in self.stats_list:
            list_dict.append(self.__parse_stats_key_info(stats_line))
        return list_dict

    def save_to_file(self, info, save_path="out/stats.cfg"):
        with open(save_path, "w") as file:
            file.write(info)

    def get_bytes_retransmit_incremental_list(self, interval, list_dicts):
        try:
            i = 0
            min_val = max_val = 0
            list_retransmit = []

            for dicts in list_dicts:
                val = dicts["bytes_retransmit"]

                if val < min_val:
                    min_val = val

                if val > max_val:
                    max_val = val

                i += 1
                if interval == i:
                    i = 0
                    print()
                    list_retransmit.append(max_val - min_val)
                    max_val = min_val = val  # Starting from the last result

            if len(dicts) % interval != 0:
                list_retransmit.append(max_val - min_val)

            # print(list_retransmit, len(list_retransmit))
            return list_retransmit

        except Exception as e:
            print("异常：", e)

    def get_target_temp_list(self, list_dicts):
        try:
            extruder_temp_list = []
            bed_temp_list = []

            i = 0
            for dicts in list_dicts:
                i += 1
                bed_temp_list.append(
                    (dicts["heater_bed"]["target"], dicts["heater_bed"]["temp"])
                )
                extruder_temp_list.append(
                    (dicts["extruder"]["target"], dicts["extruder"]["temp"])
                )

            # print(extruder_temp_list)
            return (extruder_temp_list, bed_temp_list)

        except Exception as e:
            print("异常：", e)
