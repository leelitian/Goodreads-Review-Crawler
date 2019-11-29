import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def save_html(book_name, book_id, page_number, html_text):
    """
    :param book_name:   书名：如"红楼梦"
    :param book_id:     书的ID，如"014044372X"
    :param page_number: 评论页的页号，如"2"
    :param html_text:   该页的html文本
    :return:            将html文本写入.\htmls\红楼梦\014044372X_2.html
    """

    dir_path = r'./htmls/' + book_name
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    html_path = r'./htmls/' + book_name + r'/' + book_id + r'_' + page_number + r'.html'
    print(book_id + r'_' + page_number + r'.html')
    with open(html_path, "w", encoding='utf-8') as f:
        f.write(html_text)


def fetch_htmls(book_name, book_id):
    """
    :param book_name: 书名，如'水浒传'
    :param book_id: 书的ID，如"18883038"
    :return: 将爬取到的所有html文件写入./htmls/book_name/book_id_page_number.html
    """

    # 打开浏览器：https://www.goodreads.com/book/show/18883038
    option = webdriver.ChromeOptions()
    option.add_argument('headless')  # 设置option
    driver = webdriver.Chrome(chrome_options=option)
    # driver = webdriver.Chrome()
    driver.get('https://www.goodreads.com/book/show/' + book_id)

    # 有的网页会弹出注册界面，尝试将其关闭
    try:
        WebDriverWait(driver, 30).until(
            ec.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div[1]/button'))).click()
    except:
        pass

    # 分页爬取评论
    page_number = 0
    while True:
        page_number = page_number + 1

        time.sleep(5)
        save_html(book_name, book_id, str(page_number), driver.page_source)

        # 尝试点击next_page超链接
        try:
            element = WebDriverWait(driver, 30).until(
                ec.element_to_be_clickable((By.CLASS_NAME, 'next_page')))
        except:
            return

        # print(element.get_attribute('class'))
        if element.get_attribute('class') != 'next_page':
            break

        driver.execute_script("arguments[0].click();", element)
        # element.click()

    os.system('taskkill /im chromedriver.exe /F')
    os.system('taskkill /im chrome.exe /F')


def fetch_all_books_htmls():
    root_dir = './ids'
    file_list = os.listdir(root_dir)  # 列出文件夹下所有的目录与文件
    for file_name in file_list:
        fpath = os.path.join(root_dir, file_name)
        with open(fpath, 'r') as f:
            text = f.read()
            id_list = text.split()

        book_name = file_name[:-4]
        print('获取html文本：{0}'.format(book_name))

        for book_id in id_list:
            fetch_htmls(book_name, book_id)


def main():
    fetch_all_books_htmls()


if __name__ == '__main__':
    # main()
    os.system('taskkill /im chromedriver.exe /F')
    os.system('taskkill /im chrome.exe /F')
    # fetch_htmls('红楼梦', '243900')
    main()
