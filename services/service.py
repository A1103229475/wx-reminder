import json

from common.request import request
from common.load_env import get_string
from configs.config import memorial_config
from common.utils import get_time_dif, get_anniversary_distance, get_now_time, get_hex_by_chinese_name, index_score

class WXService:
    def __init__(self):
        self.appID = get_string('appID')
        self.appsecret = get_string('appsecret')

    def send(self, template_id, msg_data):
        access_token = self.get_access_token()
        url = f'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}'
        data = {
            "touser": "o5x_m5v-5Ug3lm4FpFO7Y53AXCRw",
            "template_id": template_id,
            "data": msg_data
        }
        print(data)
        result = request('post', url, data)
        print(result.json())
        return result

    def send_everyday_reminder(self):
        """
        {{datetime.DATA}}
        今天是我们相恋的第{{love_day_dif.DATA}}天
        距离我们的恋爱纪念日还有{{love_day_distance.DATA}}天
        距离你的生日还有{{birthday_dif.DATA}}天
        {{weather.city.DATA}}当前天气 {{weather.text.DATA}}
        当前温度 {{weather.temp.DATA}}
        风向 {{weather.wind_dir.DATA}}
        风力等级 {{weather.wind_class.DATA}}

        每日一句：
        {{one_sentence.DATA}}
        """
        template_id = '63mlV_13rIboFU7J-Jc5_qjlaJQIzwvV_jJrHLFH31Y'
        now_time = get_now_time()
        love_day_dif = self.get_love_day()
        love_day_distance = self.get_love_day_distance()['distance']
        birthday_dif = self.get_birth_day_distance()['distance']
        weather = self.get_weather()
        one_sentence = self.get_one_sentence()
        print(one_sentence)
        data = {
            'datetime': {
                "value": now_time,
                "color": "#FF88C2"
            },
            'love_day_dif': {
                'value': love_day_dif,
                "color": "#FF0000"
            },
            'love_day_distance': {
                'value': love_day_distance,
                "color": "#FF5511"
            },
            'birthday_dif': {
                'value': birthday_dif,
                "color": "#FF8800"
            },
            'weather': {
                'city': {
                    'value': weather['location']['city']+weather['location']['name'],
                    "color": "#173177"
                },
                'text': {
                    'value': weather['now']['text'],
                    "color": "#00DD00"
                },
                'temp': {
                    'value': weather['now']['temp'],
                    "color": "#A500CC"
                },
                'wind_dir': {
                    'value': weather['now']['wind_dir'],
                    "color": "#7700BB"
                },
                'wind_class': {
                    'value': weather['now']['wind_class'],
                    "color": "#A500CC"
                }
            },
            'one_sentence':{
                'value':one_sentence,
                "color": "#FF8800"
            }
        }
        return self.send(template_id, data)

    def send_today_weather_reminder(self):
        """
        {{datetime.DATA}}
        {{weather.city.DATA}}
        今日天气 {{weather.text.DATA}}
        今日温度 {{weather.temp.DATA}}
        风力等级 {{weather.wind.DATA}}

        老公提醒你: {{reminder.DATA}}
        """
        template_id = '0bL0IHfgvdEblGaGbAYKUfqKwIINyNOmP2jzsHRnTQE'
        weather = self.get_weather()
        now_time = get_now_time()
        city = weather['location']['province'] + weather['location']['city'] + weather['location']['name']
        text_day = weather['forecasts'][0]['text_day']
        text_night = weather['forecasts'][0]['text_night']
        text = text_day if text_day == text_night else f"{text_day}-{text_night}"
        high = weather['forecasts'][0]['high']
        low = weather['forecasts'][0]['low']
        temp = f"{high}℃" if high == low else f"{low}℃-{high}℃"
        wc_day = weather['forecasts'][0]['wc_day']
        wc_night = weather['forecasts'][0]['wc_night']
        wind = wc_day if wc_day == wc_night else f"{wc_day}-{wc_night}"

        reminder = ""
        print(high, type(high), low, type(low))
        if "雨" in text:
            reminder += '今天有雨，记得带伞哦~'
        if high >= 26 and low >= 20:
            reminder += '天气偏热，注意防暑，记得涂防晒！'
        elif high < 26 and low < 20:
            reminder += '温度较低，注意保暖哦~'

        data = {
            'datetime': {
                "value": now_time,
                "color": "#FF88C2"
            },
            'weather': {
                'city': {
                    "value": city,
                    "color": "#0044BB"
                },
                'text': {
                    "value": text,
                    "color": "#00DD00"
                },
                'temp': {
                    "value": temp,
                    "color": "#A500CC"
                },
                'wind': {
                    "value": wind,
                    "color": "#7700BB"
                }
            },
            'reminder': {
                "value": reminder,
                "color": "#FF8800"
            }
        }
        return self.send(template_id, data)

    def send_today_constellation(self, cons_name: str = '摩羯座'):
        """
        {{datetime.DATA}}
        {{name.DATA}}今日运势↓
        幸运色 {{color.DATA}}
        健康指数 {{health.DATA}}
        爱情指数 {{love.DATA}}
        财运指数 {{money.DATA}}
        工作指数 {{work.DATA}}
        幸运数字 {{number.DATA}}
        速配星座 {{QFriend.DATA}}
        总结 {{summary.DATA}}
        :return:
        """
        template_id = 'fPUZdOfISuAxDHA562_5bzgupnD6XaZGnW6xC2vzNFU'
        now_time = get_now_time()
        constellation = self.get_constellation(cons_name)
        data = {
            'datetime': {
                "value": now_time,
                "color": "#FF88C2"
            },
            'name': {
                "value": constellation['name'],
                "color": "#FFC0CB"
            },
            'color': {
                "value": constellation['color'],
                "color": get_hex_by_chinese_name(constellation['color'])
            },
            'health': {
                "value": constellation['health'],
                "color": index_score(constellation['health'])
            },
            'money': {
                "value": constellation['money'],
                "color": index_score(constellation['money'])
            },
            'love': {
                "value": constellation['love'],
                "color": index_score(constellation['love'])
            },
            'work': {
                "value": constellation['work'],
                "color": index_score(constellation['work'])
            },
            'number': {
                "value": constellation['number'],
                "color": "#173177"
            },
            'QFriend': {
                "value": constellation['QFriend'],
                "color": "#9400D3"
            },
            'summary': {
                "value": constellation['summary'],
                "color": "#FF8800"
            },
        }
        return self.send(template_id, data)

    def send_week_constellation(self, cons_name: str = '摩羯座'):
        """
        {{datetime.DATA}}
        {{name.DATA}} 本周{{date.DATA}}运势↓
        健康方面 {{health.DATA}}
        感情方面 {{love.DATA}}
        财运方面 {{money.DATA}}
        工作方面 {{work.DATA}}
        职场方面 {{job.DATA}}
        :return:
        """
        template_id = 'sW3Whu32HGPTrGiYNEhQHzQLXdniaKf_Xiw8o0KqYeQ'
        now_time = get_now_time()
        constellation = self.get_constellation(cons_name, type='week')
        data = {
            'datetime': {
                "value": now_time,
                "color": "#FF88C2"
            },
            'name': {
                "value": constellation['name'],
                "color": "#FFC0CB"
            },
            'date': {
                "value": constellation['date'],
                "color": "#FFC0CB"
            },
            'health': {
                "value": constellation['health'],
                "color": "#FF8800"
            },
            'love': {
                "value": constellation['love'],
                "color": "#FF8800"
            },
            'money': {
                "value": constellation['money'],
                "color": "#FF8800"
            },
            'work': {
                "value": constellation['work'],
                "color": "#FF8800"
            },
            'job': {
                "value": constellation['love'],
                "color": "#FF8800"
            },
        }
        return self.send(template_id, data)

    def get_access_token(self):
        url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.appID}&secret={self.appsecret}'
        access_token = request('get', url).json()['access_token']
        return access_token

    # 获取恋爱纪念日间隔
    def get_love_day_distance(self) -> dict:
        try:
            love_time = memorial_config['memorial_day']['love_time']
            love_day_distance = get_anniversary_distance(love_time)
            return love_day_distance
        except Exception as e:
            print(e)
            return {}

    # 获取相恋天数
    def get_love_day(self) -> str:
        try:
            love_time = memorial_config['memorial_day']['love_time']
            time_dif = get_time_dif(love_time, 'day')

            return time_dif
        except Exception as e:
            print(e)
            return '获取相恋天数失败'

    # 获取相恋年数
    def get_love_year(self) -> str:
        try:
            love_time = memorial_config['memorial_day']['love_time']
            love_year = get_time_dif(love_time, 'year')

            return str(love_year)
        except Exception as e:
            print(e)
            return '获取相恋年数失败'

    # 获取生日距离
    def get_birth_day_distance(self) -> dict or None:
        try:
            birthday = memorial_config['my_baby']['solar_birthday']
            birthday_dif = get_anniversary_distance(birthday)
            return birthday_dif
        except Exception as e:
            print(e)
            return None

    # 获取天气
    def get_weather(self, city='深圳') -> dict:
        try:
            baidu_ak = get_string('baidu_ak')
            district_id = 440307

            url = f'https://api.map.baidu.com/weather/v1/?district_id={district_id}&data_type=all&ak={baidu_ak}'
            weather = request('get', url).json()
            return weather['result']
        except Exception as e:
            print(e)
            return {}

    # 获取每日一句
    def get_one_sentence(self) -> str:
        try:
            url = 'https://v1.hitokoto.cn/'
            result = request('get', url).json()
            if not result:
                return '今天的句子很短，我爱你'
            return result['hitokoto']
        except Exception as e:
            print(e)
            return '今天的句子很短，我爱你'

    # 获取星座运势
    def get_constellation(self, cons_name: str = '摩羯座', type: str = 'today') -> dict or None:
        # type= today,tomorrow,week,month,year
        juhe_constellation_key = get_string('juhe_constellation_key')
        url = f'http://web.juhe.cn/constellation/getAll?consName={cons_name}&type={type}&key={juhe_constellation_key}'
        result = request('get', url).json()

        return result