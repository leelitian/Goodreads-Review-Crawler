import re
import requests
import json
import os


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


def get_ids_by_string(book_name, search_string):
    """
    :param book_name:       书名：红楼梦
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

        regex = re.compile('"url" href="/book/show/\d+')
        raw_id_list = regex.findall(text)

        ids_path = r'./ids/' + book_name + '.txt'
        with open(ids_path, "a", encoding='utf-8') as f:
            for raw_id in raw_id_list:
                f.write(raw_id[23:] + '\n')


def get_ids_by_json():
    """
    :return: 从books.json中读取{ book_name : search_strings_list }，
            并将搜索到的book_id写入./ids/book_name.txt
    """
    str_file = './books.json'
    with open(str_file, 'r', encoding='utf-8') as f:
        # print("Load str file from {}".format(str_file))
        book_dict = json.load(f)

    for book_name in book_dict.keys():
        search_string_list = book_dict[book_name]
        for search_string in search_string_list:
            get_ids_by_string(book_name, search_string)
        print('{0}.txt获取成功！'.format(book_name))


def unique_ids(fpath):
    """
    :param fpath: 文件的路径
    :return:      对fpath文件当中的ids进行去重
    """
    with open(fpath, 'r') as f:
        text = f.read()
        tmp_list = text.split()

    res_list = list(set(tmp_list))
    with open(fpath, 'w') as f:
        for url in res_list:
            f.write(url + '\n')


def unique_all_books_ids():
    """
    :return: 对所有的book_name.txt当中的ids进行去重
    """
    root_dir = './ids'
    file_list = os.listdir(root_dir)  # 列出文件夹下所有的目录与文件
    for file_name in file_list:
        fpath = os.path.join(root_dir, file_name)
        unique_ids(fpath)


def main():
    get_ids_by_json()
    unique_all_books_ids()


if __name__ == '__main__':
    main()
