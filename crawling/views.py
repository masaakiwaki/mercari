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
    drivepath = os.path.join(os.path.dirname(
        os.path.abspath('__file__')), ('chromedriver.exe'))
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(drivepath, options=options)

# create file_name (now data,time)


def File_Name(output_name):
    dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    fdt_now = dt_now.strftime('%Y%m%d%H%M%S')
    file_name = os.path.join(os.path.dirname(
        os.path.abspath('__file__')), (fdt_now + "_" + output_name))
    return file_name


'''
dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
fdt_now = dt_now.strftime('%Y%m%d%H%M%S')
file_name = os.path.dirname(os.path.abspath('__file__'))
print(file_name)




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
'''


class Item_Detail():
    def __init__(self):
        self.info_number = ''
        self.find_tag = ''

    driver.get('https://www.mercari.com/jp/items/m28554804613/')

    def screen_capture(self):
        page_width = driver.execute_script('return document.body.scrollWidth')
        page_height = driver.execute_script(
            'return document.body.scrollHeight')
        driver.set_window_size(page_width, page_height)
        #capture_name = File_Name('screen.png')
        capture_name = 'media/screen.png'
        driver.save_screenshot(capture_name)
        return

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
        list_object = []
        for i in info:
            i = i.select("th")
        list_object.append(i[0].get_text())
        return list_object

    def detail_contents(self, info_number, find_tag):
        list_object = []
        info = self.detail_information()
        i = info[info_number].select(find_tag)
        for i in i:
            i = i.get_text()
            i = i.replace('\n', '')  # 　delete indention
            i = i.replace(' ', '')  # 　delete space
            list_object.append(i)
        return list_object

    def detail_contents_list(self):
        list_object = []

        user_list = []
        '''information user name'''
        user_list.append(self.detail_contents(0, 'a'))

        '''information user valuation'''
        user_list.append(self.detail_contents(0, 'span'))
        list_object.append(user_list)

        '''information category name'''
        list_object.append(self.detail_contents(1, 'div'))

        '''information category brand'''
        list_object.append(self.detail_contents(2, 'div'))

        '''information category status'''
        list_object.append(self.detail_contents(3, 'td'))

        '''information category shipping'''
        list_object.append(self.detail_contents(4, 'td'))

        '''information category shipping method'''
        list_object.append(self.detail_contents(5, 'td'))

        '''information category shipping method'''
        list_object.append(self.detail_contents(6, 'td'))

        '''information category shipping day'''
        list_object.append(self.detail_contents(7, 'td'))
        return list_object

    def flatten(self, l):
        import collections
        for el in l:
            if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
                yield from self.flatten(el)
            else:
                yield el

    def create_csv(self):
        list_heder = ['タイトル', 'ヘッダー', '本文', '価格', '税区分', '送料', 'いいね', '出品者', '高評価', '低評価',
                      'カテゴリー1', 'カテゴリー2', 'カテゴリー3', 'ブランド', '商品の状態', '配送料の負担', '配送の方法', '配送元地域', '発送日の目安']

        list_object = []
        list_object.append(self.detail_title())
        list_object.append(self.detail_heder())
        list_object.append(self.detail_text())
        list_object.append(self.detail_price())
        list_object.append(self.detail_like())
        list_object.append(self.detail_contents_list())
        list_object = list(self.flatten(list_object))

        with open("detail.csv", "w", encoding="utf-8") as f:  # 文字コードをShift_JISに指定
            # writerオブジェクトの作成 改行記号で行を区切る
            writer = csv.writer(f, lineterminator="\n")
            writer.writerow(list_heder)  # csvファイルに書き込み
            writer.writerow(list_object)  # csvファイルに書き込み

        return list_heder, list_object


def Scraping(request):
    global list_object
    a = Item_Detail()
    a.screen_capture()
    list_object = a.create_csv()
    dict_object = dict(zip(list_object[0], list_object[1]))

    dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    fdt_now = dt_now.strftime(
        '%Y' + '年' + '%m' + '月' + '%d' + '日' + '%H' + '時' + '%M' + '分' + '%S' + '秒')

    content = {
        'message': fdt_now + '時点のYahoo Japanトップページのニュース一覧です。',
        'detail_dict': dict_object,
    }
    driver.close()
    return render(request, 'crawling/index.html', content)


def Download_List(request):
    # レスポンスの設定
    csv_object = [list_object[0], list_object[1]]
    response = HttpResponse(content_type='text/csv')
    filename = 'YahooNewsList.csv'  # ダウンロードするcsvファイル名
    response['Content-Disposition'] = 'attachment; filename={}'.format(
        filename)
    writer = csv.writer(response)
    writer.writerows(csv_object)
    return response


if __name__ == "__main__":
    main()
