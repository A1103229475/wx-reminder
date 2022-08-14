import datetime
from configs.config import week_list, color_list

def get_now_time():
    now_time = datetime.datetime.now()
    now_time_str = f'{now_time.year}年{now_time.month}月{now_time.day}日 {week_list[now_time.weekday()]}'
    return now_time_str

def get_time_dif(time: str, type: str):
    now_time = datetime.datetime.now()
    now_time = now_time.strftime('%Y-%m-%d')
    now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d')
    time = datetime.datetime.strptime(time, '%Y-%m-%d')
    time_dif = now_time - time
    if type == 'day':
        return abs(int(time_dif.days))
    elif type == 'year':
        return abs(int(int(time_dif.days) / 365))

def get_anniversary_distance(time: str):
    now_time = datetime.datetime.now()
    now_time = now_time.strftime('%Y-%m-%d')
    now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d')
    time = datetime.datetime.strptime(time, '%Y-%m-%d')
    # 将时间转成下次纪念日的时间
    year = now_time.year
    if now_time.month > time.month or (now_time.month == time.month and now_time.day > time.day):
        year = year + 1
    convert_time = datetime.datetime.strptime(f'{year}-{time.month}-{time.day}', '%Y-%m-%d')
    result = {
        'is_birthday': False,   # 今天是否生日
        'distance': abs(int((now_time - convert_time).days)),  # 距离生日多少天
        'birthday_count': year - time.year # 第几个生日
    }

    if time.month == now_time.month and time.day == now_time.day:
        result['is_birthday'] = True
        return result

    return result

def get_hex_by_chinese_name(chinese_name):
    for color in color_list:
        if color['chinese_name'] == chinese_name:
            return color['hex'].strip()
    return '#87CEEB'

def index_score(index: int or str):
    index = int(index)
    if index >=  90:
        return '#FF1493'
    else:
        return '#FF69B4'