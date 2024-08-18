dicts = {"heater_bed": {"target": 60, "temp": 55}}

val_list = []

# 选择一种方法添加多个值
val_list.extend([dicts["heater_bed"]["target"], dicts["heater_bed"]["temp"]])

print(val_list)  # 输出: [60, 55]
