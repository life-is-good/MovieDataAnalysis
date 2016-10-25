# -*- coding:utf-8 -*-
import urllib2
from scrapy.selector import Selector
from douban_maoyan_time_config import *
import bson
import time

# 代理
def proxy_request(url):
    request = urllib2.urlopen(url)
    return request.read()

def human_info(info_dict):
    data = proxy_request(info_dict['url'])
    sel = Selector(text=data)
    print u'URL:%s' % info_dict['url']
    get_dict = human_info_format()
    get_dict['human_url'] = info_dict['url']
    get_dict['Releate_ID'] = info_dict['url'].split('/')[-2].strip()
    # 照片
    get_dict['img_url'] = sel.xpath('//*[@id="headline"]//*[@class="pic"]/a/img/@src').extract()[0].strip()
    print u'照片URL:%s' % get_dict['img_url']
    #get_dict['img_data'] = bson.Binary(urllib2.urlopen(get_dict['img_url']).read())
    # 中文名和英文名
    name = sel.xpath('//*[@id="content"]/h1/text()').extract()[0].strip()
    print u'名字:%s' % name
    name_list = name.split(' ')
    get_dict['cn_name'] = name_list[0]
    print u'中文名:%s' % get_dict['cn_name']
    name_list.pop(0)
    get_dict['en_name'] = ' '.join(name_list)
    print u'英文名:%s' % get_dict['en_name']

    # 其余信息
    for i in sel.xpath('//*[@id="headline"]//*[@class="info"]/ul/li'):
        for j in douban_human_dict:
            if i.xpath('./span/text()').extract()[0].strip() == douban_human_dict[j]:
                source_info = i.xpath('./text()').extract()
                if source_info:
                    source_info = i.xpath('./text()').extract()[1].strip().split(':')[1].strip()
                    get_dict[j] = source_info
                    print u'{0}\t\t{1}'.format(j, get_dict[j])

                    if i.xpath('./span/text()').extract()[0].strip() == u'imdb编号':
                        get_dict['IMDB_ID'] = dict()
                        get_dict['IMDB_ID']['name'] = i.xpath('./a/text()').extract()[0].strip()
                        get_dict['IMDB_ID']['url'] = i.xpath('./a/@href').extract()[0].strip()
                        print u'imdb编号:{0}链接:{1}'.format(get_dict['IMDB_ID']['name'], get_dict['IMDB_ID']['url'])
    # 简介
    all_introduce = sel.xpath('//*[@class="all hidden"]/text() | //*[@id="intro"]//*[@class="bd"]/text()').extract()
    if all_introduce:
        get_dict['introduce'] = all_introduce
        for kk in all_introduce:
            print kk
    # 全部作品
    print u'=======================全部作品情况======================'
    history_works_record(info_dict['movie_id'])
    print u'=======================全部获奖情况======================'
    # 获奖情况
    history_awards_info(info_dict['movie_id'])

# 历史作品总数
def history_works_record(movie_id):
    history_works_list = list()
    new_url = 'https://movie.douban.com/celebrity/{0}/movies?start=0&format=pic&sortby=time&'.format(movie_id)
    data = proxy_request(new_url)
    sel = Selector(text=data)
    history_works_list.extend(history_info(sel))
    all_count = int(sel.xpath('//*[@class="count"]/text()').extract()[0].strip().split(u'共')[1].split(u'条')[0].strip())
    print u'一共的条数:%s' % all_count

    for i in range(1, all_count / 10 + 1):
        new_url = 'https://movie.douban.com/celebrity/{0}/movies?start={1}&format=pic&sortby=time&'.format(movie_id,i * 10)
        data = proxy_request(new_url)
        sel = Selector(text=data)
        history_works_list.extend(history_info(sel))
    #print len(history_works_list)


# 作品页面解析 缺IMDB编号
def history_info(sel):
    works_list = list()
    for i in sel.xpath('//*[@ class="grid_view"]/ul/li'):
        works_dict = dict()
        works_dict['name'] = i.xpath('./dl/dd/h6/a/text()').extract()[0].strip()
        print u'作品名称:%s' % works_dict['name']
        works_dict['works_url'] = i.xpath('./dl/dd/h6/a/@href').extract()[0].strip()
        print u'作品链接:%s' % works_dict['works_url']
        if len(i.xpath('./dl/dd/h6/span')) == 3:

            works_dict['date'] = i.xpath('./dl/dd/h6/span[1]/text()').extract()[0].strip()
            print u'作品时间:%s' % works_dict['date']
            works_dict['status'] = i.xpath('./dl/dd/h6/span[2]/text()').extract()[0].strip()
            print u'状态:%s' % works_dict['status']
            works_dict['position'] = i.xpath('./dl/dd/h6/span[3]/text()').extract()[0].strip()
            print u'职能:%s' % works_dict['position']
        else:
            works_dict['date'] = i.xpath('./dl/dd/h6/span[1]/text()').extract()[0].strip()
            print u'作品时间:%s' % works_dict['date']
            works_dict['status'] = u'已上映'
            works_dict['position'] = i.xpath('./dl/dd/h6/span[2]/text()').extract()[0].strip()
            print u'职能:%s' % works_dict['position']
        works_list.append(works_dict)

        f = open(u'周星驰作品.txt','a')
        f.write(u'作品名称：  '+works_dict['name'])
        f.write('\n')
        f.write(u'作品链接：  '+works_dict['works_url'])
        f.write('\n')
        f.write(u'作品时间：  '+works_dict['status'])
        f.write('\n')
        f.write(u'作品职能：  '+works_dict['position'])
        f.write('\n')
        f.write('=====================================')
        f.write('\n')
        print '-------' * 5

    return works_list


# 获奖记录 缺IMDB编号
def history_awards_info(movie_id):
    url = 'https://movie.douban.com/celebrity/{0}/awards/'.format(movie_id)
    data = proxy_request(url)
    sel = Selector(text=data)
    all_awards_list = list()
    for i in sel.xpath('//*[@id="content"]//*[@class="article"]/div'):
        awards_dict = dict()
        awards_dict['date'] = str()
        awards_dict['award_introduce'] = list()
        awards_dict['date'] = i.xpath('./div/h2/text()').extract()[0].strip()
        print u'年份:%s' % awards_dict['date']
        for j in i.xpath('.//*[@class="award"]'):
            single_record = dict()
            single_record['award_body'] = str()
            single_record['award_name'] = str()
            single_record['film_info'] = dict()
            single_record['award_body'] = j.xpath('./li[1]/a/text()').extract()[0].strip()
            print u'类型:%s' % single_record['award_body']
            single_record['award_name'] = j.xpath('./li[2]/text()').extract()[0].strip()
            print u'奖项:%s' % single_record['award_name']
            single_record['film_info']['name'] = j.xpath('./li[3]/a/text()').extract()[0].strip()
            print u'获奖作品:%s' % single_record['film_info']['name']
            single_record['film_info']['url'] = j.xpath('./li[3]/a/@href').extract()[0].strip()
            print u'获奖作品链接:%s' % single_record['film_info']['url']

            f = open(u'周星驰获奖作品.txt', 'a')
            f.write(u'年份：  ' + awards_dict['date'])
            f.write('\n')
            f.write(u'类型：  ' + single_record['award_body'])
            f.write('\n')
            f.write(u'奖项：  ' + single_record['award_name'])
            f.write('\n')
            f.write(u'获奖作品：  ' + single_record['film_info']['name'])
            f.write('\n')
            f.write(u'获奖作品链接：  ' + single_record['film_info']['url'])
            f.write('\n')
            f.write('=====================================')
            f.write('\n')
            print '----------------' * 5


human_info({'name': u'周星驰', 'url': 'https://movie.douban.com/celebrity/1048026/', 'movie_id': '1048026'})