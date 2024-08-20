from PyQt5.QtCore import QThread, pyqtSignal, Qt


class AnalysisThread(QThread):
    analysis_complete = pyqtSignal(list, str, list)  
    error_occurred = pyqtSignal(str)  

    def __init__(self, log, view_model, task_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_type = task_type
        self.log = log
        self.view_model = view_model

    def bind_event(self, complete_event, error_event):
        self.analysis_complete.connect(complete_event)
        self.error_occurred.connect(error_event)

    def stop(self):
        self.wait()

    def run(self):
        try:
            if self.task_type == "comprehensive_analysis":
                result = self.view_model.comprehensive_analysis(self.log)
            elif self.task_type == "loss_packet_analysis":
                result = self.view_model.loss_packet_analysis(self.log)

            mcu_list = self.view_model.get_mcu_list(self.log)
            self.analysis_complete.emit(
                result, self.task_type, mcu_list
            )  #Transmit completion signal
        except Exception as e:
            self.error_occurred.emit(str(e))  #Send error signal
