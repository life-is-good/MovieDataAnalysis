# -*- coding: utf-8 -*-
import urllib
import urllib2
from scrapy.selector import Selector
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#猫眼票房数据存储格式
def cateye_info():
        data = dict()
        '''基本数据字段'''
        #每日票房
        data['day_box_office'] = str()
        #每日排片占比
        data['day_percent'] = str()
        #场均人次
        data['per_people'] = str()
        #总票房
        data['all_box_office'] = str()
        #首周票房
        data['first_week_box_office'] = str()
        #点映票房
        data['point_release_box_office'] = str()
        #每日排片场次
        data['day_release_times'] = str()
        #城市票房数据
        data['city_box_office'] = list()
        #城市票房占比
        data['city_box_office_percent'] = list()
        #城市排片占比
        data['city_percent'] = list()
        #城市累计票房
        data['city_total_box_office'] = list()
        #电影猫眼URL
        data['url'] = str()
        #电影名称
        data['name'] = str()
        return data

#猫眼信息
def maoyan_info(url):
    response = urllib2.urlopen(url)
    sel = Selector(text=response.read())
    data = cateye_info()
    data['url'] = url
    print u'来源URL:%s' % data['url']
    data['all_box_office'] = sel.xpath('//*[@class="tags clearfix"]/span/i/text()').extract()[0].strip()
    print u'总票房:%s' % data['all_box_office']

    # 日票房信息
    all_day = sel.xpath('//*[@id="ticketList"]//*[@id="ticket_tbody"]/ul')
    for i in all_day:
        date = i.xpath('./li[1]/span/b/text()').extract()[0].strip()
        print u'日期:%s' % date
        day_box_officce = i.xpath('./li[2]/i/text()').extract()[0].strip()
        print u'当日票房:%s' % day_box_officce
        day_box_officce_percent = i.xpath('./li[3]/i/text()').extract()[0].strip()
        print u'票房占比:%s' % day_box_officce_percent
        day_release_percent = i.xpath('./li[4]/i/text()').extract()[0].strip()
        print u'排片占比:%s' % day_release_percent
        day_people = i.xpath('./li[5]/i/text()').extract()[0].strip()
        print u'场均人次:%s' % day_people

        print '-------' * 5


# 城市信息
def city_info(date):
    url = 'http://piaofang.maoyan.com/movie/338391/cityBox?date={0}'.format(date)

    json_data = json.loads(urllib2.urlopen(url).read())
    sel = Selector(text=json_data['html'])
    all_info = sel.xpath('//*[@class="m-table normal m-table-city"]/tbody/tr')
    for i in all_info:
        city = i.xpath('./td[1]/text()').extract()[0].strip()
        print u'城市:%s' % city
        box_office = i.xpath('./td[2]/i/text()').extract()[0].strip()
        print u'票房:%s' % box_office
        box_office_percent = i.xpath('./td[3]/i/text()').extract()[0].strip()
        print u'票房占比:%s' % box_office_percent
        release_percent = i.xpath('./td[4]/i/text()').extract()[0].strip()
        print u'排片占比:%s' % release_percent
        total_box_office = i.xpath('./td[5]/i/text()').extract()[0].strip()
        print u'累计票房:%s' % total_box_office
        position_percent = i.xpath('./td[6]/i/text()').extract()[0].strip()
        print u'排座占比:%s' % position_percent
        gold_percent = i.xpath('./td[7]/i/text()').extract()[0].strip()
        print u'黄金场占比:%s' % gold_percent
        per_people = i.xpath('./td[8]/i/text()').extract()[0].strip()
        print u'场均人次:%s' % per_people
        people = i.xpath('./td[9]/i/text()').extract()[0].strip()
        print u'人次:%s' % people
        times = i.xpath('./td[10]/i/text()').extract()[0].strip()
        print u'场次:%s' % times
        print unichr(int('4F60',16))

        print '-------------' * 5

city_info('2016-10-7')
#maoyan_info('http://piaofang.maoyan.com/movie/338391')


def search_film(name):
    url = 'http://piaofang.maoyan.com/search?key=%s' % name
    print u'路径:%s' % url
    url1 = urllib.urlencode({'ok': '魔兽'})

    # url = 'http://piaofang.maoyan.com/search?key=%E4%B8%96%E7%95%8C%E6%97%A6%E5%A4%95%E4%B9%8B%E9%97%B4'

    data = urllib2.urlopen(url).read()
    # print data
    sel = Selector(text=data)
    # print sel.xpath('//*[@id="search-list"]/article')
    for i in sel.xpath('//*[@id="search-list"]/article'):
        movie_name = i.xpath('.//*[@class="title"]/text()').extract()[0].strip()
        print u'电影名称:%s' % movie_name
        date = i.xpath('./text()').extract()[2].strip()
        print u'时间:%s' % date
        movie_url = 'http://piaofang.maoyan.com' + i.xpath('./@data-url').extract()[0].strip()
        print u'电影URL:%s' % movie_url
        print '---------' * 5


#search_film('魔兽')