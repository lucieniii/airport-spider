# coding=utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json
import codecs
import os
import matplotlib.pyplot as plt
import time


def time_to_num(t):
    t = t.split(":")
    return int(t[0]) + int(t[1]) / 60.0


def daily_report_gen(time_table):
    # 图表生成

    x = []
    pt_all = []
    at_all = []
    latency_dict = {}
    for i in range(24):
        x.append(i)
        pt_all.append(0)
        at_all.append(0)
    for it in time_table:
        pt_all[int(it['pt'])] += 1
        if it['at']:
            at_all[int(it['at'])] += 1
            la = int((it['at'] - it['pt']) * 60)
            latency_dict[str(la)] = latency_dict.get(str(la), 0) + 1
    latency_x = [-0.5, -0.25, 0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5]
    latency_y = [ 0,    0, 0,   0, 0,   0, 0,   0, 0,   0, 0,   0, 0]
    cnt = 0
    tot = 0
    for key, value in latency_dict.items():
        lt = int(key)
        cnt += value
        tot += value * lt
        if lt == 0:
            pass
        elif lt < 0:
            lt /= 60.0
            if lt <= -1:
                latency_y[0] += value
            else:
                latency_y[1] += value
        else:
            lt /= 60.0
            if lt >= 5:
                latency_y[12] += value
            else:
                for i in range(2, 12):
                    if latency_x[i] <= lt < latency_x[i + 1]:
                        latency_y[i] += value
                        break

    today = time.strftime("%Y-%m-%d", time.localtime())
    today_dir = 'log/' + today
    plt.plot(x, pt_all)
    plt.xlabel('time')
    plt.ylabel('number of flights')
    plt.title(today + ' Departure plan')
    plt.savefig(today_dir + "/Departure-Plan.png")
    plt.cla()

    plt.plot(x, at_all)
    plt.xlabel('time')
    plt.ylabel('number of flights')
    plt.title(today + ' Actual departure time')
    plt.savefig(today_dir + "/Actual-Departure-Time.png")
    plt.cla()

    plt.xlabel('Delay time')
    plt.ylabel('number of flights')
    plt.title(today + ' Today\'s delay, average delay time is ' + str(int(tot/cnt)) + 'minutes')
    plt.plot(latency_x, latency_y)
    plt.savefig(today_dir + "/Flight-Delay.png")
    plt.cla()

    plt.xlabel('Delay time')
    plt.ylabel('number of flights')
    plt.title(today + ' Today\'s delay more than 0.5h')
    plt.plot(latency_x[4:], latency_y[4:])
    plt.savefig(today_dir + "/Flight-Delay-More-Than-Half-An-Hour.png")

    return


class ShAirportPipeline:

    def __init__(self):
        today = time.strftime("%Y-%m-%d", time.localtime())
        today_dir = 'log/' + today
        if not os.path.exists(today_dir):
            os.makedirs(today_dir)
        self.file = codecs.open(today_dir + '/sh-airport.json', 'w', encoding='utf-8')
        self.file.write("[\n")
        self.time_table = []

    def process_item(self, item, spider):
        # 图表生成和json文件生成
        di = dict(item)
        t = {'pt': time_to_num(di['plan_departure_time'])}
        at = di['actual_departure_time']
        if '实际出发' in at:
            t['at'] = time_to_num(at[4:])
        else:
            t['at'] = None
        self.time_table.append(t)
        line = json.dumps(di, ensure_ascii=False) + ",\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.seek(-2, os.SEEK_END)
        self.file.truncate()
        self.file.seek(0, os.SEEK_END)
        self.file.write('\n]')
        print(self.time_table)
        daily_report_gen(self.time_table)
        self.file.close()
        print("Successfully crawled data.")
