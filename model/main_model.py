

class MainViewModel:
    def __init__(self):
        self.intervel = 100

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
            paser.paser_cfg()

    def set_intervel(self, intervel):
        self.intervel = intervel

    def comprehensive_analysis(self, log):
        subplot_data = []
        if log != "":
            paser = PaserLog(log)
            subplot_data.append(paser.analysis_bytes_retransmit(self.intervel))
            subplot_data.append(paser.analysis_bed_temp())
            subplot_data.append(paser.analysis_extruder_temp())

        return subplot_data

    def loss_packet_analysis(self, log):
        subplot_data = []
        if log != "":
            paser = PaserLog(log)
            subplot_data.append(paser.analysis_bytes_retransmit(100))
        return subplot_data
