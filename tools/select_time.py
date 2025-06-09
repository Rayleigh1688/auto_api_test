import datetime

start = datetime.datetime(2025, 5, 8)
end = datetime.datetime(2025, 6, 5)

start_ts = int(start.timestamp() * 1000)
end_ts = int(end.timestamp() * 1000)

print("开始时间戳（毫秒）:", start_ts)
print("结束时间戳（毫秒）:", end_ts)