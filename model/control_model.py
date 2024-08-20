'''
@File    :   control_model.py
@Time    :   2024/08/21
@Desc    :   Process module data needed for the control view interface
'''


from concurrent.futures import ThreadPoolExecutor
import time
from model.common import GlobalComm, Utilities
from model.parse import PaserLog


class ControlModel:
    def __init__(self):
        self.intervel = int(GlobalComm.setting_json["loss_interval_set"]) #default value
        self.mcu_info = ""

    def get_error_str(self, log):
        paser = PaserLog(log)
        return paser.paser_error()

    def output_analysis_result(self, log):
        if log != "":
            paser = PaserLog(log)
            paser.paser_cfg()
            paser.paser_stats()
            paser.paser_error()
            paser.paser_shucdown_info()

    def output_cfg(self, log):
        if log != "":
            paser = PaserLog(log)
            return paser.paser_cfg()
        return ""

    def get_cfg_info(self, log):
        if log != "":
            paser = PaserLog(log)
            return paser.paser_cfg_info()
        return ""

    def get_mcu_list(self, log):
        if log != "":
            paser = PaserLog(log)
            return paser.paser_mcu()
        return []

    def output_main_cfg_info(self, log, file_update):
        """Get the main information in klipper.cfg
           -> Currently obtain mcu related information

        Args:
            log (str): klippy.log information
            file_update (bool): Select whether the file has changed

        Returns:
            str: mcu related information
        """
        if file_update or self.mcu_info == "":
            cfg = self.get_cfg_info(log)
            self.mcu_info = ""
            extracted_lines = []
            capture = False
            lines = cfg.split("\n")
            for line in lines:
                #Check if it is a line starting with [mcu
                if line.startswith("[mcu") or line.startswith("[beacon]"):
                    capture = True

                #If between [mcu and serial, capture line
                if capture:
                    extracted_lines.append(line)

                #Check if it is a line starting with serial
                if "serial" in line or "canbus_uuid" in line:
                    capture = False
            self.mcu_info = "\n".join(extracted_lines)
        return self.mcu_info

    def set_intervel(self, intervel):
        self.intervel = intervel

    def comprehensive_analysis(self, log):
        subplot_data = []
        if log != "":
            paser = PaserLog(log)
            subplot_data.append(paser.analysis_bytes_retransmit(self.intervel))
            subplot_data.append(paser.analysis_bed_temp(self.intervel))
            subplot_data.append(paser.analysis_extruder_temp(self.intervel))

        return subplot_data

    def loss_packet_analysis(self, log):
        subplot_data = []
        if log != "":
            paser = PaserLog(log)
            subplot_data.append(paser.analysis_bytes_retransmit(self.intervel))
        return subplot_data

    def save_files(self, path, only_cfg=False):
        log = ""
        with open(path, "r", encoding="utf-8") as file:
            log = file.read()

        if only_cfg:
            self.output_analysis_result(log)
        else:
            self.output_cfg(log)

    def print_count(self, path):
        target_strings = [
            GlobalComm.setting_json["starting_sd_print"],
            GlobalComm.setting_json["finish_sd_print"],
        ]

        counts = {target: 0 for target in target_strings}

        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                for target in target_strings:
                    counts[target] += line.count(target)

        return counts

    def update_current_log(self, cur_file_path, cur_newest_path):
        log = ""
        if cur_file_path != cur_newest_path:
            with open(cur_newest_path, "r", encoding="utf-8") as file:
                log = file.read()
        return log
