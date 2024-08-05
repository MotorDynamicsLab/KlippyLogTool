from paser_log.paser_log import LogKlipper, LogStats
import matplotlib.pyplot as plt

if __name__ == "__main__":
    file_path = "./logs/klippy.log"

    log = ""
    with open(file_path, "r") as file:
        log = file.read()

    cfg = LogKlipper(log)
    klipper_cfg = cfg.extract_newest_config()
    cfg.save_to_file(klipper_cfg)

    stats = LogStats(file_path)
    list_dicts = stats.get_stats_dicts()
    stats.save_to_file(stats.get_stats_info())

    stats_out_path = "./out/stats.cfg"
    stats = LogStats(stats_out_path)
    list_dicts = stats.get_stats_dicts()

    try:
        interval = 100  # sampling interval
        i = 0
        min_val = max_val = 0
        list_retransmit = [0]
        min_last_val = max_last_val = 0

        for dicts in list_dicts:
            min_last_val = min(
                dicts["bytes_retransmit"]
            )  # Here min_last_val and max_last_val are generally the same value
            max_last_val = max(dicts["bytes_retransmit"])

            if min_last_val < min_val:
                min_val = min_last_val

            if max_last_val > max_val:
                max_val = max_last_val

            i += 1
            if interval == i:
                i = 0
                list_retransmit.append(max_val - min_val)
                min_val = min_last_val  # Starting from the last result
                max_val = max_last_val

        if len(dicts) % interval != 0:
            list_retransmit.append(max_val - min_val)
        print(list_retransmit, len(list_retransmit))

    except Exception as e:
        print("异常：", e)

    # 画图
    plt.plot(list_retransmit)

    # 添加标题和标签
    plt.title("折线图示例")
    plt.xlabel("索引")
    plt.ylabel("值")

    # 显示图形
    plt.show()
