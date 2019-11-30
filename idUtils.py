import re
import requests
import json
import os
from operator import itemgetter
from itertools import groupby
from bs4 import BeautifulSoup


def get_html(url):
    """
    :param url: 网址url
    :return:    从网址url获得的html文本
    """
    try_times = 40
    while try_times != 0:
        r = requests.get(url, timeout=40)
        r.encoding = "UTF-8"
        if r.status_code == 200:
            # print('getHTML Success')
            return r.text
        else:
            try_times = try_times - 1
    print('getHTML Error')
    return ""


id_dict_list = []


def id_crawler(text):
    """
    :param text: html文本
    :return: 获取在html文本当中的书籍信息{ 'name' = '红楼梦', 'id' = '12345', author = ['cao xue qin', 'aaa']}，
             并加入id_dict_list
    """
    soup = BeautifulSoup(text, 'lxml')

    for book in soup.find_all(name='tr', attrs={'itemtype': "http://schema.org/Book"}):
        id_dict = {}

        title = book.find(name='a', attrs={'class': "bookTitle"})

        name = title.get_text()
        name = name.replace('\n', '').replace('\r', '')
        id_dict['name'] = name

        regex = re.compile('/book/show/\d+')
        href = title['href']
        book_id = regex.findall(href)[0][11:]
        id_dict['id'] = book_id

        authors = book.find_all(name='a', attrs={'class': "authorName"})
        author_list = []
        for author in authors:
            author_name = author.get_text()
            author_list.append(author_name)
        id_dict['authors'] = author_list

        id_dict_list.append(id_dict)


def get_ids_by_string(search_string):
    """
    :param search_string:  搜索的字符串：A Dream in Red Mansions
    :return:    搜索A Dream in Red Mansions得到一个book_id列表，追加写入./ids/book_name.txt
    """

    # TODO:       这里设置了搜索页数为1，如何过滤不合理的book_id呢
    max_page_number = 1
    # https://www.goodreads.com/search?q=A+Dream+in+Red+Mansions&search_type=books&page=

    search_string = search_string.replace(' ', '+')
    raw_url = 'https://www.goodreads.com/search?q=' + search_string + '&search_type=books&page='
    page_number = 0

    while page_number < max_page_number:
        page_number = page_number + 1
        url = raw_url + str(page_number)
        text = get_html(url)
        id_crawler(text)


def get_ids_by_json():
    """
    :return: 从books.json中读取{ book_name : search_strings_list }，
            并将搜索到的book_id的信息写入./ids/book_name.json
    """
    str_file = './books.json'
    with open(str_file, 'r', encoding='utf-8') as f:
        # print("Load str file from {}".format(str_file))
        book_dict = json.load(f)

    for book_name in book_dict.keys():
        search_string_list = book_dict[book_name]
        for search_string in search_string_list:
            get_ids_by_string(search_string)

        id_path = './ids/' + book_name + '.json'
        unique_ids()

        with open(id_path, "w", encoding='utf-8') as f:
            json.dump(id_dict_list, f, ensure_ascii=False)
        id_dict_list.clear()

        print('{0}.json获取成功！'.format(book_name))


def unique_ids():
    """
    :return:  对于json文件，以每本书的id作为key进行去重
    """

    global id_dict_list
    key = itemgetter('id')
    items = sorted(id_dict_list, key=key)
    id_dict_list = [next(v) for _, v in groupby(items, key=key)]


def main():
    get_ids_by_json()


if __name__ == '__main__':
    main()
