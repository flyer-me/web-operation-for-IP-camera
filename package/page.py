from DrissionPage import ChromiumOptions, SessionOptions, WebPage

def init():
    co = ChromiumOptions(ini_path=r'.\config\web-config.ini')
    co = co.ignore_certificate_errors()
    so = SessionOptions(ini_path=r'.\config\web-config.ini')
    return WebPage(chromium_options=co, session_or_options=so)