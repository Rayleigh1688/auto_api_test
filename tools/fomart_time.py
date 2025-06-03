import datetime
import calendar

# 设置东八区
from datetime import timezone, timedelta
TZ = timezone(timedelta(hours=8))  # 东八区

def datetime_to_unix_ms(dt: datetime.datetime):
    return int(dt.astimezone(datetime.timezone.utc).timestamp() * 1000)

def show_human_readable(ts_ms):
    dt = datetime.datetime.fromtimestamp(ts_ms / 1000, tz=TZ)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def get_time_ranges():
    now = datetime.datetime.now(TZ)
    today_start = datetime.datetime.combine(now.date(), datetime.time.min, tzinfo=TZ)
    today_end = datetime.datetime.combine(now.date(), datetime.time.max, tzinfo=TZ)

    yesterday_date = now.date() - datetime.timedelta(days=1)
    yesterday_start = datetime.datetime.combine(yesterday_date, datetime.time.min, tzinfo=TZ)
    yesterday_end = datetime.datetime.combine(yesterday_date, datetime.time.max, tzinfo=TZ)

    week_start = today_start - datetime.timedelta(days=today_start.weekday())
    week_end = week_start + datetime.timedelta(days=6, hours=23, minutes=59, seconds=59, microseconds=999999)

    month_start = today_start.replace(day=1)
    last_day = calendar.monthrange(now.year, now.month)[1]
    month_end = today_start.replace(day=last_day, hour=23, minute=59, second=59, microsecond=999999)

    if now.month == 1:
        last_month_year = now.year - 1
        last_month = 12
    else:
        last_month_year = now.year
        last_month = now.month - 1

    last_month_start = datetime.datetime(last_month_year, last_month, 1, tzinfo=TZ)
    last_month_end_day = calendar.monthrange(last_month_year, last_month)[1]
    last_month_end = datetime.datetime(
        last_month_year, last_month, last_month_end_day,
        hour=23, minute=59, second=59, microsecond=999999, tzinfo=TZ
    )

    return {
        "today": {
            "start": datetime_to_unix_ms(today_start),
            "end": datetime_to_unix_ms(today_end)
        },
        "yesterday": {
            "start": datetime_to_unix_ms(yesterday_start),
            "end": datetime_to_unix_ms(yesterday_end)
        },
        "week": {
            "start": datetime_to_unix_ms(week_start),
            "end": datetime_to_unix_ms(week_end)
        },
        "month": {
            "start": datetime_to_unix_ms(month_start),
            "end": datetime_to_unix_ms(month_end)
        },
        "last_month": {
            "start": datetime_to_unix_ms(last_month_start),
            "end": datetime_to_unix_ms(last_month_end)
        }
    }
# 数据库查询，常用时间戳。
if __name__ == "__main__":
    time_ranges = get_time_ranges()
    for label, times in time_ranges.items():
        print(f"{label.upper()}:")
        print(f"  Start: {times['start']}  ({show_human_readable(times['start'])})")
        print(f"  End:   {times['end']}  ({show_human_readable(times['end'])})\n")