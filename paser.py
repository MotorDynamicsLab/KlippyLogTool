from paser_log.paser_log import LogKlipper, LogStats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors

if __name__ == "__main__":
    file_path = "./logs/klippy11.log"

    log = ""
    with open(file_path, "r", encoding="utf-8") as file:
        log = file.read()

    cfg = LogKlipper(log)
    klipper_cfg = cfg.extract_newest_config()
    cfg.save_to_file(klipper_cfg)
    cfg.save_to_file(cfg.get_stats_shucdown_info(), "out/error.txt")

    # 保存到文件
    stats = LogStats(log)
    list_dicts = stats.get_stats_dicts()
    LogKlipper.save_to_file(stats.get_stats_info(), "out/stats.cfg")

    # 解析out的文件
    list_retransmit = stats.get_bytes_retransmit_incremental_list(100, list_dicts)

    # 画图
    x_odd1 = range(len(list_retransmit))

    plt.subplot(2, 1, 1)
    plt.title("bytes retransmit magnitude of change")
    plt.xlabel("statistical intervals")
    plt.ylabel("value of change")
    (line,) = plt.plot(
        x_odd1,
        list_retransmit,
    )
    mplcursors.cursor([line], hover=True)

    #############################################
    extruder_temp_list, bed_temp_list = stats.get_target_temp_list(list_dicts)
    target_extruder_list = [t[0] for t in extruder_temp_list]
    temp_extruder_list = [t[1] for t in extruder_temp_list]

    target_bed_list = [t[0] for t in bed_temp_list]
    temp_bed_list = [t[1] for t in bed_temp_list]

    # 计算移动平均
    target_extruder = pd.Series(target_extruder_list)
    temp_extruder = pd.Series(temp_extruder_list)
    target_bed_list = pd.Series(target_bed_list)
    temp_bed_list = pd.Series(temp_bed_list)

    # 计算移动平均
    target_extruder_mean = target_extruder.rolling(window=100).mean()
    temp_extruder_mean = temp_extruder.rolling(window=100).mean()

    target_bed_mean = target_bed_list.rolling(window=100).mean()
    temp_bed_mean = temp_bed_list.rolling(window=100).mean()

    # 绘制原始数据和移动平均线

    ax1 = plt.subplot(2, 2, 3)
    plt.title("extruder temp")
    plt.xlabel("stats count")
    plt.ylabel("temp")
    ax1.legend()
    (line1,) = ax1.plot(
        target_extruder_mean.index,
        target_extruder_mean,
        label="target extruder",
        linestyle="--",
        color="b",
    )
    (line2,) = ax1.plot(
        temp_extruder_mean.index,
        temp_extruder_mean,
        label="temp extruder",
        color="r",
    )
    ax1.legend(loc="upper right")
    mplcursors.cursor([line1, line2], hover=True)

    ax2 = plt.subplot(2, 2, 4)
    plt.title("bed temp")
    plt.xlabel("stats count")
    plt.ylabel("temp")
    ax2.legend()
    (line3,) = ax2.plot(
        target_bed_mean.index,
        target_bed_mean,
        label="target bed",
        linestyle="--",
        color="g",
    )
    (line4,) = ax2.plot(
        temp_bed_mean.index,
        temp_bed_mean,
        label="temp bed",
        color="orange",
    )
    ax2.legend(loc="upper right")
    mplcursors.cursor([line3, line4], hover=True)

    # 显示图形
    plt.tight_layout()
    plt.show()
