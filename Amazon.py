import requests
from bs4 import BeautifulSoup
import re

page_count = 0
review_count = 0
isLegal = True
comments_dict = {}


def isEmpty(str):
    for c in str:
        if c.isalnum():
            return False
    return True


def getHTMLText(url):  # 获取HTML页面，请求50次;请求失败，则返回空
    try_times = 50
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


def crawURL(one_book_url_list):  # 根据书的主页url进行爬取
    global page_count, isLegal

    done = 0
    total = len(one_book_url_list)

    for url in one_book_url_list:
        page_count = 0
        isLegal = True
        # print('>>> ', url)
        getOneBook(url)
        done = done + 1
        print("当前进度：{0}/{1}".format(done, total))


def getOneBook(one_book_url):  # 通过一本书主页的url，生成若干评论页url，并爬取
    global page_count

    suffix1 = "/ref=cm_cr_arp_d_paging_btm_next_"  # 下一页的后缀
    suffix2 = "?pageNumber="

    while isLegal:
        page_count = page_count + 1
        one_page_url = one_book_url + suffix1 + str(page_count) + suffix2 + str(page_count)  # 最终的评论页url
        getReview(one_page_url)
        # print("已完成页数", page_count)

    # print("... 共找到评论：", review_count)


def getReview(one_page_url):  # 处理好评论页的HTML文件，将评论写到文件中
    global isLegal, review_count

    review_page = getHTMLText(one_page_url)

    # 爬取星级
    regex1 = re.compile('"review-star-rating" class="a-icon a-icon-star a-star-\d')
    star_list = regex1.findall(review_page)
    for i in range(len(star_list)):
        star_list[i] = star_list[i][-1]
    star_index = -1

    # 爬取评论
    regex2 = re.compile('<br\s*?/?>')
    demo = regex2.sub(' ', review_page)  # 将<br>替换为空格

    isLegal = False  # 假设此页面不存在评论
    soup = BeautifulSoup(demo, 'lxml')  # 解析

    for span in soup.find_all("span"):  # 对于所有的<span>标签,如果它有一个键值对为{'data-hook':'review-body'}
        try:
            if span.attrs['data-hook'] == 'review-body':
                isLegal = True  # 则发现评论
                for kids in span.children:  # 评论隐藏在它的子标签里
                    if isEmpty(kids.string):
                        continue
                    review_count = review_count + 1
                    star_index = star_index + 1
                    # with open(comments_file, 'a', encoding='utf-8') as f:  # 写入文件
                    comment = r'"' + kids.string.replace('\"', '\'') + r'"'
                    url = r'"' + one_page_url + r'"'
                    star = str(star_list[star_index])
                    comments_dict[comment] = [url, star]
                    # f.write(rid + r',' + comment + r',' + url + r',' + star + '\n')
        except:
            continue


def writeFile(comments_file):  # 将字典中的键值对写入文件
    ids = 0
    with open(comments_file, 'w', encoding='utf-8') as f:
        f.write("id,comment,url,star\n")
        for comment in comments_dict.keys():
            ids = ids + 1
            f.write(
                str(ids) + r',' + comment + r',' + comments_dict[comment][0] + r',' + comments_dict[comment][1] + '\n')

    print("写入完成，去重后共找到{0}条评论".format(ids))


def getBookBySearch(search_page_url_list, search_url_file):  # 在亚马逊的搜索页中查找相应书的url，并产生主页的url
    one_book_url_list = []
    for url in search_page_url_list:
        demo = getHTMLText(url)
        soup = BeautifulSoup(demo, 'lxml')

        for span in soup.find_all('span'):
            try:
                if span.attrs['data-component-type'] == 's-product-image':
                    for kids in span.children:
                        if kids.name == 'a':
                            one_book_url_list.append("https://www.amazon.com" + kids.attrs['href'])
            except:
                pass

    for i in range(len(one_book_url_list)):
        one_book_url_list[i] = one_book_url_list[i].replace("/dp/", "/product-reviews/")
        with open(search_url_file, 'a') as f:
            print(one_book_url_list[i])
            f.write(one_book_url_list[i] + '\n')


def getBookByFile(fpath):  # 从文件中读取文件主页
    with open(fpath, 'r') as f:
        text = f.read()
        return text.split()


def uniqueURLs(fpath):  # 对文件中的url去重
    with open(fpath, 'r') as f:
        text = f.read()
        tmp_list = text.split()

    res_list = list(set(tmp_list))
    with open(fpath, 'w') as f:
        for url in res_list:
            f.write(url + '\n')


#   if __name__ == '__main__':

    # search_page_url_list = ['https://www.amazon.com/s?k=The+Tale+of+Genji&rh=p_n_feature_nine_browse-bin%3A3291437011&dc&page=4&qid=1558710570&rnid=3291435011&ref=sr_pg_4']

    # 从search_page_url_list中获取书并写入文件
    # getBookBySearch(search_page_url_list, r'comment_urls_Genji.txt')
    # uniqueURLs(r'comment_urls_ThreeKingdoms.txt')

    # # 水浒传
    # one_book_url_list = getBookByFile(r'.\comment_urls_WaterMargin.txt')  # 从book_urls.txt获取书
    # crawURL(one_book_url_list)  # 对书进行爬取
    # writeFile(r'./Water Margins.csv')
    # comments_dict.clear()
    #
    # # 西游记
    # one_book_url_list = getBookByFile(r'.\comment_urls_WestJourney.txt')  # 从book_urls.txt获取书
    # crawURL(one_book_url_list)  # 对书进行爬取
    # writeFile(r'./The Journey To The West.csv')
    # comments_dict.clear()
    #
    # # 红楼梦
    # one_book_url_list = getBookByFile(r'.\comment_urls_RedMansions.txt')  # 从book_urls.txt获取书
    # crawURL(one_book_url_list)  # 对书进行爬取
    # writeFile(r'./The Dream of Red Mansions.csv')
    # comments_dict.clear()
    #
    # # 三国演义
    # one_book_url_list = getBookByFile(r'.\comment_urls_ThreeKingdoms.txt')  # 从book_urls.txt获取书
    # crawURL(one_book_url_list)  # 对书进行爬取
    # writeFile(r'./Romance of Three Kingdoms.csv')
    # comments_dict.clear()

    # 源氏物语
    # one_book_url_list = getBookByFile(r'.\comment_urls_Genji.txt')  # 从book_urls.txt获取书
    # crawURL(one_book_url_list)  # 对书进行爬取
    # writeFile(r'./源氏物语.csv')