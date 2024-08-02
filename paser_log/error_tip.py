class ErrorTip:
    def __init__(self, error, tip):
        self.error = error

    def get_newest_error(log):
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
