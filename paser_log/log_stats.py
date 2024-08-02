import re
from collections import defaultdict


class LogStats:
    def __init__(self, log_path):
        self.log_path = log_path

    def __parse_stats_info(stats_string):
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

    def __generate_stats_list(self):
        out = []
        try:
            with open(self.log_path, "r") as file:
                for line in file:
                    if line.startswith("Stats"):
                        out.append(line.strip())
            return out
        except FileNotFoundError:
            return "错误: 文件未找到"

    def get_stats_dicts(self):
        list = self.__generate_stats_list()
        line_dicts = []
        for line in list:
            line_dicts.append(self.__parse_stats_info(line))
        return line_dicts
