from paser_log.error_tip import ErrorTip
from paser_log.extract_cfg import KlipperCfg
from paser_log.log_stats import LogStats


if __name__ == "__main__":
    file_path = "./logs/klippy.log"

    cfg = KlipperCfg(file_path)
    cfg.open_log_file()
    cfg.save_config()

    statsMsg = LogStats(file_path)
    statsMsg.open_log_file()
    # print(statsMsg.get_stats_dicts())

    errorTip = ErrorTip(file_path)
    print(errorTip.get_newest_error(cfg.get_log_info()))

    # target_bed, target_extruder = get_last_target_temp(out_log)
    # print(target_bed, target_extruder)

    # print(get_error_tip(out_log))
    # print_stats_lines(file_path)
    # # print(result)
