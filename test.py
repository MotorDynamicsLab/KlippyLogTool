import matplotlib.pyplot as plt
import random


# 生成随机颜色的函数
def random_color():
    return (random.random(), random.random(), random.random())


# 示例数据
list_retransmit = [1, 2, 3, 4, 5]
list_mcu1 = [10, 20, 30, 40, 50]
list_mcu2 = [15, 25, 35, 45, 55]

# 创建一个空的 plot_data 列表
plot_data = []

color = random_color()

# 添加第一个数据集
plot_data.append(
    {
        "x": list(range(len(list_retransmit))),
        "y": list_mcu1,
        "label": "MCU1",
        "linestyle": "-",
        "color": random_color(),
    }
)

# 添加第二个数据集
plot_data.append(
    {
        "x": list(range(len(list_retransmit))),
        "y": list_mcu2,
        "label": "MCU2",
        "linestyle": "--",
        "color": random_color(),
    }
)

# 绘制图形
for data in plot_data:
    plt.plot(
        data["x"],
        data["y"],
        label=data["label"],
        linestyle=data["linestyle"],
        color=data["color"],
    )

# 添加图例
plt.legend()

# 显示图形
plt.show()
