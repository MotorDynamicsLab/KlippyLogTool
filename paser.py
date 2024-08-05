from paser_log.log_stats import LogKlipper, LogStats


if __name__ == "__main__":
    file_path = "./logs/klippy.log"

    file = open(file_path, "r")
    log = file.read()

    cfg = LogKlipper(log)
    klipper_cfg = cfg.extract_newest_config()
    cfg.save_config(klipper_cfg)
