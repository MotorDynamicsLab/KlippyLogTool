import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import mplcursors

# 设置中文字体
font_path = 'C:/Windows/Fonts/simhei.ttf'  # Windows 系统上的字体路径
prop = fm.FontProperties(fname=font_path)

# 模拟数据
data1 = {
    "x": [1, 2, 3, 4, 5],
    "y": [2, 3, 5, 7, 11],
    "label": "图1标签",
    "color": "blue",
    "linestyle": "-"
}

data2 = {
    "x": [1, 2, 3, 4, 5],
    "y": [1, 4, 6, 8, 10],
    "label": "图2标签",
    "color": "red",
    "linestyle": "--"
}

# 创建图形对象
fig, ax = plt.subplots()

# 绘制图形1
line1, = ax.plot(
    data1["x"],
    data1["y"],
    label=data1["label"],
    color=data1["color"],
    linestyle=data1["linestyle"]
)
line1.label = data1["label"]

# 绘制图形2
line2, = ax.plot(
    data2["x"],
    data2["y"],
    label=data2["label"],
    color=data2["color"],
    linestyle=data2["linestyle"]
)
line2.label = data2["label"]

# 设置图例，使用中文字体
ax.legend(prop=prop)

# 设置标题和坐标轴标签
ax.set_title('中文标题', fontproperties=prop)
ax.set_xlabel('X轴标签', fontproperties=prop)
ax.set_ylabel('Y轴标签', fontproperties=prop)

# 使用 mplcursors 添加悬停标签
cursor = mplcursors.cursor([line1, line2], hover=True)

@cursor.connect("add")
def on_add(sel):
    x, y = sel.target
    line = sel.artist
    sel.annotation.set_text(f'{line.label}\nX: {x}\nY: {y}')
    sel.annotation.set_fontproperties(prop)

# 显示图形
plt.show()