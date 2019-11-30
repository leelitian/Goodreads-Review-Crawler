# GoodReads评论爬取

### 处理的流程

#### idUtils.py

* 解析books.json，获取相关书籍相关的搜索字符串(e.g. A Dream of Red Mansion)
* 根据搜索字符串在页面进行搜索，将获取到的`{书名，书的id，作者}`存放到**book_name.json**文件下
* 根据人工筛选，得到正确的书籍列表
* TODO：搜索页数设置为了2，需不需要修改？

#### htmlUtils.py

* 从**ids文件夹**下的json文件中获取书籍的id
* 利用selenium获取每个book_id的评论页面
* 将获取到的HTML页面保存在htmls文件夹中，命名为`book_id`_`page_number`.html

#### crawlerUtils.py

* 利用BeatifulSoup解析获取到的html页面，并把处理好的文件放置到**src文件夹**下
* TODO：处理star/comment为空的情况

