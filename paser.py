from paser_log.paser_log import LogKlipper, LogStats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    file_path = "./logs/klippy2.log"

    log = ""
    with open(file_path, "r") as file:
        log = file.read()

    cfg = LogKlipper(log)
    klipper_cfg = cfg.extract_newest_config()
    cfg.save_to_file(klipper_cfg)

    # 保存到文件
    stats = LogStats(file_path)
    list_dicts = stats.get_stats_dicts()
    stats.save_to_file(stats.get_stats_info())

    # 解析out的文件
    stats_out_path = "./out/stats.cfg"
    stats = LogStats(stats_out_path)
    list_dicts = stats.get_stats_dicts()

    list_retransmit = stats.get_bytes_retransmit_incremental_list(100, list_dicts)

    # 画图
    x_odd1 = range(len(list_retransmit))

    # 绘制折线图
    # (line1_odd,) = plt.plot(
    #     x_odd1,
    #     list_retransmit,
    #     label="var",
    #     marker="o",
    #     linestyle="-",
    #     linewidth=1,
    # )

    # # 添加标题和标签
    # plt.title("label")
    # plt.xlabel("count")
    # plt.ylabel("var")

    # 添加鼠标悬停显示数值功能
    # mplcursors.cursor([x_odd1, line1_odd], hover=True)

    # 显示图形
    # plt.show()

    extruder_temp_list, bed_temp_list = stats.get_target_temp_list(list_dicts)
    target_extruder_list = [t[0] for t in extruder_temp_list]
    temp_extruder_list = [t[1] for t in extruder_temp_list]

    LogKlipper.save_to_file(" ".join(temp_extruder_list), "out/temp_val.cfg")

    target_bed_list = [t[0] for t in bed_temp_list]
    temp_bed_list = [t[1] for t in bed_temp_list]

    # 计算移动平均
    data = pd.Series(temp_extruder_list)
    print(data)

    # 计算移动平均
    rolling_mean = data.rolling(window=100).mean()  # 使用更大的窗口来平滑数据

    # 绘制原始数据和移动平均线
    plt.figure(figsize=(12, 6))  # 增加图表尺寸
    # plt.plot(
    #     data.index, data, label="Original Data", alpha=0.5, color="b"
    # )  # 降低原始数据的透明度
    plt.plot(
        rolling_mean.index,
        rolling_mean,
        label="Moving Average",
        linestyle="-",
        color="r",
    )

    # 调整Y轴的范围和步长
    plt.ylim(-200, 300)  # 根据数据调整Y轴范围
    plt.yticks(np.arange(-200, 300, 10))  # 设置Y轴的步长为2

    # 添加图例、标题和坐标轴标签
    plt.legend()
    plt.title("Original Data vs. Moving Average")
    plt.xlabel("Index")
    plt.ylabel("Value")

    # 显示图形
    plt.show()

# print(temp_extruder_list)

# 创建 x 轴数据
# x_odd1 = range(len(target_extruder_list))
# x_even1 = range(len(temp_extruder_list))
# x_odd2 = range(len(target_bed_list))
# x_even2 = range(len(temp_bed_list))
# print(x_odd1, x_even1)

# 绘制折线图
# plt.scatter(
#     x_odd1,
#     target_extruder_list,
#     label="target extruder",
#     linewidth=0.3,
#     color="green",
#     alpha=0.7,
# )

# plt.plot(
#     x_even1,
#     temp_extruder_list,
#     label="temp extruder",
#     linewidth=1,
#     alpha=0.7,
# )

# (line2_odd,) = plt.plot(
#     x_odd2,
#     target_bed_list,
#     label="target bed",
#     marker="o",
#     linestyle="-",
#     linewidth=1,
# )
# (line2_even,) = plt.plot(
#     x_even2,
#     temp_bed_list,
#     label="temp bed",
#     linewidth=0.3,
#     alpha=0.7,
# )

# 添加标题和标签
# plt.title("Odd and Even Values Line Plot for Two Lists")
# plt.xlabel("Index")
# plt.ylabel("Value")
# # plt.ylim(-330, 330)
# # plt.gca().invert_yaxis()
# plt.legend()
# plt.yticks([])
# plt.xticks([])
# 添加点击标签隐藏/显示线条的功能
# def on_pick(event):
#     line = event.artist
#     line.set_visible(not line.get_visible())
#     plt.draw()

# 添加鼠标悬停显示数值功能
# mplcursors.cursor([line1_odd, line1_even, line2_odd, line2_even], hover=True)

# # 连接点击事件
# plt.gcf().canvas.mpl_connect("pick_event", on_pick)

# # 使线条可拾取
# line1_odd.set_picker(True)
# line1_even.set_picker(True)
# line2_odd.set_picker(True)
# line2_even.set_picker(True)

# 显示图形
# plt.grid(True)
# plt.show()
