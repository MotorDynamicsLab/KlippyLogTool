from paser_log.paser_log import LogKlipper, LogStats


if __name__ == "__main__":
    file_path = "./logs/klippy.log"

    log = ""
    with open(file_path, "r") as file:
        log = file.read()

    cfg = LogKlipper(log)
    klipper_cfg = cfg.extract_newest_config()
    cfg.save_config(klipper_cfg)

    stats = LogStats(file_path)
    list_stats = stats.get_stats_dicts()
    print(list_stats)
