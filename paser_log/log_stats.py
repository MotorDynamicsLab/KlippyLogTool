import re
from collections import defaultdict


class LogStats:
    def __init__(self, log_path):
        self.log_path = log_path

    def __generate_stats_list(self):
        self.stats_list = []
        try:
            with open(self.log_path, "r") as file:
                for line in file:
                    if line.startswith("Stats"):
                        self.stats_list.append(line.strip())
        except FileNotFoundError:
            return "错误: 文件未找到"

    def open_log_file(self):
        self.__generate_stats_list()

    def get_log_info(self):
        return self

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

    def get_stats_dicts(self):
        list_dict = []
        for stats_line in self.stats_list:
            list_dict.append(self.__parse_stats_info(stats_line))
        return list_dict
