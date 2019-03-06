from wxpy import *
import requests
import urllib.request
import urllib.parse
import gzip
import json

from apscheduler.schedulers.blocking import BlockingScheduler

#bot = Bot(cache_path="mybot.pkl")


# bot = Bot()

# linux执行登陆请调用下面的这句
bot = Bot(console_qr=True ,cache_path=True)
def get_news():
    """获取金山词霸每日一句，英文和翻译"""
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    content = r.json()['content']
    note = r.json()['note']
    return content, note


def get_weather():
    citycode = 101040100
    if not citycode:
        print('未找到该城市')
        return
    url = 'http://wthrcdn.etouch.cn/weather_mini?citykey=%s' % citycode
    # print(url)
    resp = urllib.request.urlopen(url).read()
    # print(resp)
    # 因网页内容做了 gzip 压缩，所以要对其解压
    try:
        data = gzip.decompress(resp)
    except:
        data = resp
    # print(data)
    # 将 json 格式的结果转为字典对象
    result = json.loads(data)
    # print(result)
    result_data = result.get('data')
    # print(result_data)
    if result_data:

        msg = '天气预报：\n'
        forecast = result_data.get('forecast')
        fc = forecast[0]
        msg = msg + fc.get('date') + '：' + fc.get('type') + '，' + fc.get('low') + '，' + fc.get('high') + "\n\n"

        # for fc in forecast:
        #    print(fc.get('date'), '：', fc.get('type'), '，', fc.get('low'), '，', fc.get('high'))
        msg = msg + '友情提示：\n'
        msg = msg + result_data.get('ganmao')

        return msg
    else:
        print('未能获取此城市的天气情况。')


def send_msg():
    try:
        contents = get_news()
        # 你朋友的微信名称，不是备注，也不是微信帐号。
        # my_friend = bot.friends().search('罗睿')[0]
        my_groups = bot.groups().search("社会主义接班人")[0]
        #my_groups = bot.groups().search("测试")[0]
        my_groups.send("童鞋们早安！\n\n在踏上奋斗之路时\n\n请确保工牌已带上\n\n愿美好生活每一天\n\n"+get_weather()+"\n\n每日一句:\n"+contents[0]+"\n"+contents[1])

    # my_groups.send_image("gongpai.png")

    # 每86400秒（1天），发送1次
    # t = Timer(86400, send_news)
    # 为了防止时间太固定，于是决定对其加上随机数
    # ran_int = random.randint(0, 100)
    # t = Timer(10, send_news)
    # t.start()
    except:
        # 你的微信名称，不是微信帐号。
        my_friend = bot.friends().search('禾禾禾')[0]
        my_friend.send("今天消息发送失败了")


def start():
    scheduler = BlockingScheduler()
    scheduler.add_job(send_msg,'cron', day_of_week='mon-fri', hour=7, minute=30,end_date='2050-01-01')
    #scheduler.add_job(send_msg, 'cron', second='*/10', max_instances=10)
    scheduler.start()


if __name__ == "__main__":
    start()
