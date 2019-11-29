import os
from bs4 import BeautifulSoup
from operator import itemgetter
from itertools import groupby

review_list = []

star_map = {'did not like it': '1', 'it was ok': '2', 'liked it': '3', 'really liked it': '4', 'it was amazing': '5'}


def one_page_crawler(text):
    """
    :param text:    html文本，从中获取其星级和评论
    :return:        review列表，类似于 [ { 'star' : 4, 'comment' : 'nice' }, ... ]
    TODO：  处理无星级和无评论的情况
    """
    soup = BeautifulSoup(text, 'lxml')
    reviews = soup.find(name='div', attrs={'id': 'bookReviews'})  # <div id="bookReviews">

    # regex = re.compile('<br\s*?/?>')
    for review in reviews.find_all(name='div', attrs={'itemprop': 'reviews'}):
        review_dict = {}

        star = review.find_all(name='span', attrs={'class': ' staticStars notranslate'})
        if star:
            # print(star[0]['title'])
            review_dict['star'] = star_map[star[0]['title']]
        else:
            # print("null")
            review_dict['star'] = "null"

        comment = review.find(name='span', attrs={'class': 'readable'})
        if comment:
            comment_list = comment.find_all(name='span')
            demo = comment_list[-1].get_text()
            # demo = regex.sub('.', demo)  # 将<br>替换为句号
            demo = demo.replace('\n', '.').replace('\r', '.')
            # print(demo)
            review_dict['comment'] = demo
        else:
            review_dict['comment'] = "null"

        if review_dict['star'] == 'null' and review_dict['comment'] == "null":
            continue
        else:
            review_list.append(review_dict)


def write_csv(book_name):
    """
    :param book_name: 处理的书名
    :return:  将review_list中的内容写入src文件夹下的book_name.csv
    """
    csv_path = r'./src/' + book_name + '.csv'
    ids = 0
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("`stars`comments\n")
        for review_dict in review_list:
            ids = ids + 1
            f.write(str(ids) + r'`' + review_dict['star'] + r'`' + review_dict['comment'] + '\n')


def unique_review():
    """
    :return: 对评论进行去重再写入
    """
    global review_list
    key = itemgetter('comment')
    items = sorted(review_list, key=key)
    review_list = [next(v) for _, v in groupby(items, key=key)]
    print(len(review_list))


def crawl_all_books():
    """
    :return: 利用beautifulsoup处理所有保存在htmls文件夹下的html文本，
             并把处理好的book_name.csv保存在src文件夹下
    """
    root_dir = './htmls'
    book_name_list = os.listdir(root_dir)  # 列出文件夹下所有的目录与文件

    for book_name in book_name_list:
        print(book_name)
        fpath = os.path.join(root_dir, book_name)
        html_list = os.listdir(fpath)

        for html in html_list:
            html_path = os.path.join(fpath, html)
            # print(html_path)
            file = open(html_path, encoding='utf-8')
            html_text = file.read()
            one_page_crawler(html_text)

        unique_review()
        write_csv(book_name)
        review_list.clear()


def main():
    crawl_all_books()


if __name__ == '__main__':
    main()
