import re
from collections import defaultdict


class LogErrorMsg:
    def __init__(self, log) -> None:
        self.log = log

    def get_newest_error(self):
        target_str = "Reactor garbage collection:"
        start_index = self.log.rfind(target_str)

        err_info = ""
        offset = 1
        if start_index != -1:
            cur_start_index = self.log.find("\n", start_index) + offset

            while True:
                cur_end_index = self.log.find("\n", cur_start_index)
                cur_str = self.log[cur_start_index:cur_end_index].strip()
                err_info += cur_str + "\n"
                if not cur_str:
                    break
                cur_start_index = cur_end_index + offset

            return err_info
        return "警告: 没有发现错误信息"


class LogTemp:
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

    def save_to_file(self, cfg, save_path="out\klipper.cfg"):
        with open(save_path, "w") as file:
            file.write(cfg)


class LogStats:
    def __init__(self, file_path) -> None:
        self.file_path = file_path

    def __generate_stats_list(self):
        self.stats_list = []
        try:
            with open(self.file_path, "r") as file:
                for line in file:
                    if line.startswith("Stats"):
                        self.stats_list.append(line.strip())
        except FileNotFoundError:
            return "错误: 文件未找到"

    def __parse_stats_info(self, stats_string):
        # Use regular expressions to find all key-value pairs, including stats values
        pattern = r"(Stats)\s([\d\.]+)|(\S+)=([\d\.]+)"
        matches = re.findall(pattern, stats_string)

        # Store matching results in a dictionary, one list for each key
        stats_dict = defaultdict(list)
        for match in matches:
            if match[0] == "Stats":
                stats_dict["Stats"].append(float(match[1]))
            else:
                key = match[2]
                value = float(match[3])
                stats_dict[key].append(value)
        return stats_dict

    def get_stats_info(self):
        self.__generate_stats_list()
        return "\n".join(self.stats_list)

    def get_stats_dicts(self):
        self.__generate_stats_list()

        list_dict = []
        for stats_line in self.stats_list:
            list_dict.append(self.__parse_stats_info(stats_line))
        return list_dict

    def save_to_file(self, info, save_path="out\stats.cfg"):
        with open(save_path, "w") as file:
            file.write(info)
