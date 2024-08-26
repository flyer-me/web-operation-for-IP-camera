
keyAttr_makers = { "ikvision":"hik",
                   "iconDH-logo":"dahua-new",
                   "login-logo-dhtech":"dahua-old",
                   "华为":"huawei",
                   """allowfullscreen="true"></iframe></body>""":"unv"

}

def init():
    from DrissionPage import ChromiumOptions,ChromiumPage
    co = ChromiumOptions().set_local_port(9222)
    co = co.ignore_certificate_errors()
    page = ChromiumPage(addr_or_opts=co,timeout=5)
    return page

def get_html(ip:str) ->str:
    page = init()
    page.get(f'http://{ip}',timeout=5, retry=0)
    page._wait_loaded(1)
    return page.html

def get_maker(html:str) ->str:
    for key in keyAttr_makers.keys():
        if key in html:
            return keyAttr_makers[key]
    return "Unknown"

if __name__ == '__main__':
    ip = '172.16.41.12'
    makers = get_maker(get_html(ip))
    print(makers)