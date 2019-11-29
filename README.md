# GoodReads评论爬取

### 处理的流程

#### idUtils.py [ 现在改为手动获取ID ]

* 解析books.json，获取相关书籍相关的搜索词
* 将搜索结果存放在ids/book_name.txt
* TODO：不相关ID的过滤问题

#### htmlUtils.py

* 从**ids文件夹**获取书籍的id
* 利用selenium获取每个book_id的评论页面
* 将获取到的HTML页面保存在htmls文件夹中，命名为`book_id`_`page_number`.html

#### crawlerUtils.py

* 利用BeatifulSoup解析获取到的html页面，并把处理好的文件放置到**src文件夹**下
* TODO：处理star/comment为空的情况