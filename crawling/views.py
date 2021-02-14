from django.http import HttpResponse
from django.shortcuts import render
from selenium import webdriver
from bs4 import BeautifulSoup
import os.path
import datetime
import pytz
import csv
import re


# webdirver config (colaboratory only)
if os.path.isfile('/app/.chromedriver/bin/chromedriver'):
    drivepath = '/app/.chromedriver/bin/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(drivepath, options=options)

### webdirver config (local setting windows) ###    
elif os.path.isfile(os.path.join(os.path.dirname(os.path.abspath('__file__')), ('chromedriver.exe'))):
    drivepath = os.path.join(os.path.dirname(os.path.abspath('__file__')), ('chromedriver.exe'))
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(drivepath, options=options)

# create file_name (now data,time)


def File_Name(output_name):
    dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    fdt_now = dt_now.strftime('%Y%m%d%H%M%S')
    file_name = os.path.join(os.path.dirname(
        os.path.abspath('__file__')), (fdt_now + "_" + output_name))
    return file_name


dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
fdt_now = dt_now.strftime('%Y%m%d%H%M%S')
file_name = os.path.dirname(os.path.abspath('__file__'))
print(file_name)

'''Generate　URL'''


def search_url(keyword='not_keyword'):

    keyword = keyword

    if 'not_keyword' == keyword:
        print('検索キーワードが指定されていません')

    else:
        url = 'https://www.mercari.com/jp/search/?keyword='
        find_keyword = keyword
        generatel_url = url + keyword
        return generatel_url


get_url = search_url('django')
driver.get(get_url)
# get HTML
html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html, 'lxml')

links = [url.get('href')
         for url in soup.find_all(href=re.compile("/jp/items/m"))]
print(links)
url = [s.replace('/jp/items/m', 'https://www.mercari.com/jp/items/m')
       for s in links]
print(url)


class Item_Detail():
    def __init__(self):
        self.info_number = ''
        self.find_tag = ''

    driver.get('https://www.mercari.com/jp/items/m80585751959/')

    def get_html(self):
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        return soup

    def detail_title(self):
        i = self.get_html().select("[class='item-name']")
        i = i[0].get_text()
        return i

    def detail_heder(self):
        i = self.get_html().select("[class='item-wording']")
        i = i[0].get_text()
        return i

    def detail_text(self):
        i = self.get_html().select("[class='item-description-inner']")
        i = i[0].get_text()
        return i

    def detail_price(self):
        i = self.get_html().select("[class='item-price-box text-center']")
        price = i[0].select("span")
        list = []
        for i in price:
            list.append(i.get_text())
        return list

    def detail_like(self):
        i = self.get_html().select("[data-num='like']")
        i = i[0].get_text()
        return i

    def detail_information(self):
        '''information all'''
        i = self.get_html().select("[class='item-detail-table']")
        i = i[0].select("tr")
        return i

    def detail_categorys_list(self):
        info = self.detail_information()
        list = []
        for i in info:
            i = i.select("th")
            list.append(i[0].get_text())
        return list

    def detail_contents(self, info_number, find_tag):
        list = []
        info = self.detail_information()
        i = info[info_number].select(find_tag)
        for i in i:
            i = i.get_text()
            i = i.replace('\n', '')  # 　delete indention
            i = i.replace(' ', '')  # 　delete space
            list.append(i)
        return list

    def detail_contents_list(self):
        list = []
        list

        user_list = []
        '''information user name'''
        user_list.append(self.detail_contents(0, 'a'))

        '''information user valuation'''
        user_list.append(self.detail_contents(0, 'span'))
        list.append(user_list)

        '''information category name'''
        list.append(self.detail_contents(1, 'div'))

        '''information category brand'''
        list.append(self.detail_contents(2, 'div'))

        '''information category status'''
        list.append(self.detail_contents(3, 'td'))

        '''information category shipping'''
        list.append(self.detail_contents(4, 'td'))

        '''information category shipping method'''
        list.append(self.detail_contents(5, 'td'))

        '''information category shipping method'''
        list.append(self.detail_contents(6, 'td'))

        '''information category shipping day'''
        list.append(self.detail_contents(7, 'td'))

        return list


a = Item_Detail()

a.detail_title()

a.detail_heder()

a.detail_text()

a.detail_price()

a.detail_like()

a.detail_categorys_list()

a.detail_contents_list()


# screen capture
page_width = driver.execute_script('return document.body.scrollWidth')
page_height = driver.execute_script('return document.body.scrollHeight')
driver.set_window_size(page_width, page_height)
capture_name = File_Name('screen.png')
driver.save_screenshot(capture_name)


def Scraping(request):
    global bottest
    dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    fdt_now = dt_now.strftime(
        '%Y' + '年' + '%m' + '月' + '%d' + '日' + '%H' + '時' + '%M' + '分' + '%S' + '秒')
    bottest = Create_List()
    content = {
        'message': fdt_now + '時点のYahoo Japanトップページのニュース一覧です。',
        'htmltest': bottest[0],
    }
    return render(request, 'bot/index.html', content)


if __name__ == "__main__":
    main()
