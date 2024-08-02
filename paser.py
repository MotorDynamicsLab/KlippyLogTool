import re
from collections import defaultdict


def extract_config(file_path):
    try:
        with open(file_path, "r") as file:
            out_log = content = file.read()
            end_index = content.rfind("=======================")

            if end_index != -1:
                start_index = content.rfind("===== Config file =====", 0, end_index)
                middle_content = content[
                    start_index + len("===== Config file =====") : end_index
                ].strip()
                return middle_content, out_log
            return "警告: 未找到配置", out_log

    except FileNotFoundError:
        return "错误: 文件未找到"

    except Exception as e:
        return f"错误: {e}"


def get_temp_info(log, target_str):
    start_index = log.rfind(target_str) + len(target_str)
    if start_index != -1:
        end_index = log.find("\n", start_index)
        target_temp = log[start_index:end_index].strip()
        return target_temp
    return None


def get_last_target_temp(log):
    target_str = "Heater heater_bed approaching new target of "
    target_bed = get_temp_info(log, target_str)

    target_str = "Heater extruder approaching new target of "
    target_extruder = get_temp_info(log, target_str)
    return target_bed, target_extruder


def get_error_tip(log):
    target_str = "Reactor garbage collection:"
    start_index = log.rfind(target_str)

    err_info = ""
    offset = 1
    if start_index != -1:
        cur_start_index = log.find("\n", start_index) + offset

        while True:
            cur_end_index = log.find("\n", cur_start_index)
            cur_str = log[cur_start_index:cur_end_index].strip()
            err_info += cur_str + "\n"
            if not cur_str:
                break
            cur_start_index = cur_end_index + offset

        return err_info
    return "警告: 没有发现错误信息"


def parse_stats(stats_string):
    # 使用正则表达式查找所有键值对，包括Stats值
    pattern = r"(Stats)\s([\d\.]+)|(\S+)=([\d\.]+)"
    matches = re.findall(pattern, stats_string)

    # 将匹配结果存储在字典中，每个键对应一个列表
    stats_dict = defaultdict(list)
    for match in matches:
        if match[0] == "Stats":
            stats_dict["Stats"].append(float(match[1]))
        else:
            key = match[2]
            value = float(match[3])
            stats_dict[key].append(value)

    return stats_dict


def print_stats_lines(file_path):
    out = []
    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("Stats"):
                out.append(line.strip())

    # discode the output
    stats_dict = parse_stats(out[0])
    for key, value in stats_dict.items():
        print(f"{key}: {value}")
    print(stats_dict["Stats"])

    output_file_path = "stats.cfg"
    with open(output_file_path, "w") as file:
        for item in out:
            file.write(f"{item}\n")


if __name__ == "__main__":
    file_path = "./klippy.log"
    result, out_log = extract_config(file_path)
    target_bed, target_extruder = get_last_target_temp(out_log)
    print(target_bed, target_extruder)

    print(get_error_tip(out_log))
    print_stats_lines(file_path)
    # print(result)

    output_file_path = "klipper.cfg"
    with open(output_file_path, "w") as file:
        file.write(result)
