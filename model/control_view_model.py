from model.common import GlobalComm
from model.paser import PaserLog


class ControlViewModel:
    def __init__(self):
        self.intervel = int(GlobalComm.setting_json["loss_interval_set"])

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

    def output_main_cfg_info(self, log, file_update):
        if file_update:
            cfg = self.get_cfg_info(log)
            self.mcu_info = ""
            extracted_lines = []
            capture = False
            lines = cfg.split("\n")
            for line in lines:
                # 检查是否是[mcu开头的行
                if line.startswith("[mcu") or line.startswith("[beacon]"):
                    capture = True

                # 如果在[mcu和serial之间，捕获行
                if capture:
                    extracted_lines.append(line)

                # 检查是否是serial开头的行
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
