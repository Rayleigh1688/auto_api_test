import csv

# 模拟接口返回的数据



# 提取列表数据
response ={}
records = response.get("data", {}).get("d", [])

# 写入 CSV 文件
with open("output.csv", mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    # 写入表头
    writer.writerow(["bill_no", "bet_amount", "net_amount"])
    # 写入每行数据
    for record in records:
        writer.writerow([
            record.get("bill_no", ""),
            record.get("bet_amount", ""),
            record.get("net_amount", ""),
            record.get("net_amount", "")
        ])

print("✅ 数据已写入 output.csv")