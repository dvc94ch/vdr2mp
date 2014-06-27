from datetime import datetime, timedelta


def stringify(date_time):
    if hasattr(date_time, 'strftime'):
        return date_time.strftime('%Y-%m-%d %H:%M')
    return str(date_time)


def start_time(unix_time):
    return datetime.fromtimestamp(int(unix_time))


def end_time(date_time, duration):
    return date_time + timedelta(seconds=duration)
