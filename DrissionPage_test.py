from DrissionPage import SessionPage

from DrissionPage import ChromiumOptions, SessionOptions, WebPage

co = ChromiumOptions(ini_path=r'.\config\web-config.ini')
so = SessionOptions(ini_path=r'.\config\web-config.ini')

page = WebPage(chromium_options=co, session_or_options=so)
# 创建页面对象
page = SessionPage()

"""
# 获取 id 为 one 的元素
div1 = page.ele('#one')
# 获取 name 属性为 row1 的元素
p1 = page.ele('@name=row1')
# 获取包含“第二个div”文本的元素
div2 = page.ele('第二个div')
# 获取所有div元素
div_list = page.eles('tag:div')
# 获取到一个元素div1
div1 = page.ele('#one')

# 在div1内查找所有p元素
p_list = div1.eles('tag:p')

# 获取div1后面一个元素
div2 = div1.next()
"""
# 爬取3页
for i in range(1, 2):
    # 访问某一页的网页
    page.get(f'https://gitee.com/explore/all?page={i}')
    # 获取所有开源库<a>元素列表
    links = page.eles('.title project-namespace-path')
    # 遍历所有<a>元素
    for link in links:
        # 打印链接信息
        print(link.text, link.link)
