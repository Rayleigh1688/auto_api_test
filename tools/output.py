import pandas as pd

# 你的原始数据
data = {}

# 提取所有日期的数据
records = data["data"]["d"]

# 转换为 DataFrame
df = pd.DataFrame(records)

# 写入 CSV 文件
df.to_csv("all_days_report.csv", index=False)

# 写入 Excel 文件
# df.to_excel("all_days_report.xlsx", index=False)

print("所有日期的数据已导出为 CSV 和 Excel 文件。")