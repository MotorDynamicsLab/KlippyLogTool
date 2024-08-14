import re


class LogStats:
    def __init__(self, log) -> None:
        self.log = log

    def __generate_stats_list(self):
        self.stats_list = []
        lines = self.log.split("\n")
        self.stats_list = [line for line in lines if line.startswith("Stats")]

    def __parse_stats_key_info(self, stats_string):
        out_dicts = {}
        heater_bed_match = re.search(
            r"heater_bed:\s*target=(\d+)\s*temp=([-+]?\d*\.\d+|\d+)", stats_string
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
            out_dicts["bytes_retransmit"] = bytes_retransmit_list
        else:
            out_dicts["bytes_retransmit"] = [0]

        return out_dicts

    def get_stats_dicts(self):
        self.__generate_stats_list()

        list_dict = []
        for stats_line in self.stats_list:
            list_dict.append(self.__parse_stats_key_info(stats_line))
        return list_dict


# 读取 stats.txt 文件内容
with open("d:/sync_workspace/company/parse-klippy-log-env/out/stats.txt", "r") as file:
    log_content = file.read()

# 创建 LogStats 对象并提取数据
log_stats = LogStats(log_content)
stats_dicts = log_stats.get_stats_dicts()

# 提取 heater_bed 的 target 和 temp 数据
heater_bed_data = [
    (d["heater_bed"]["target"], d["heater_bed"]["temp"]) for d in stats_dicts
]

# 打印结果
for target, temp in heater_bed_data:
    print(f"Target: {target}, Temp: {temp}")
