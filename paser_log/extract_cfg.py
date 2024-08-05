class KlipperCfg:
    def __init__(self, log_path):
        self.log_path = log_path

    def open_log_file(self):
        try:
            with open(self.log_path, "r") as file:
                self.log = file.read()
        except FileNotFoundError:
            return "错误: 文件未找到"

    def get_log_info(self):
        return self.log

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

    def save_config(self, save_path="klipper.cfg"):
        with open(save_path, "w") as file:
            file.write(self.extract_newest_config())

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
