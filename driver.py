import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222

def init():
    """
    Initializes the webdriver with specified options and settings.

    Returns:
        driver (WebDriver): The initialized webdriver instance.
    """
    path = Service('chromedriver.exe')
    options = Options()
    options.add_argument('disable-notifications')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--log-level=3')
    options.add_argument('--headless')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-impl-side-painting')
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(service=path,options=options)
    driver.implicitly_wait(6)
    driver.maximize_window()
    return driver


def _get_attribute_of_element(element, name='textContent') -> str:
    """
    获取元素的属性值。

    Args:
        element: 元素对象。
        name: 属性名称，默认为'textContent'。

    Returns:
        元素的属性值。

    Raises:
        Exception: 获取属性值失败。
    """
    global fail_count
    try:
        return element.get_attribute(name)  # 不要使用innerText
    except Exception:
        fail_count = fail_count + 1
        raise Exception("_get_attribute失败")

def _click(driver, value: str, by=By.XPATH) -> bool:
    """
    根据给定的定位值和定位策略，点击元素。

    Args:
        driver: The WebDriver instance.
        value (str): 定位所需str的值.
        by (By): 定位策略,默认为By.XPATH.

    Returns:
        bool: 成功则返回True,否则raise exception.

    Raises:
        Exception: 点击失败.
    """
    global fail_count
    try:
        element = driver.find_element(by, value=value)
        try:
            element.click()
            time.sleep(0.01)
        except Exception:
            driver.execute_script("arguments[0].scrollIntoView();", element)
            driver.execute_script("(arguments[0]).click();", element)
    except Exception:
        fail_count = fail_count + 1
        raise Exception(f"点击value={value},by={str(by)}失败")
    return True