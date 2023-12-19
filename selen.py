import random
import time
import zipfile

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import secure

url = 'https://www.novostroyki-spb.ru/'

'''
    Строка поиска новостроек 
'''
def get_find_box(driver: webdriver.Chrome):
    el = None
    try:
        el = driver.find_element(By.XPATH, "//input[@placeholder='Поиск новостроек']")
    except NoSuchElementException:
        pass
    return el


'''
    Кнопка найти новостройки
'''
def get_but_find(driver: webdriver.Chrome):
    el = None
    try:
        el = driver.find_element(By.XPATH, "//button[contains(text(), 'Найти')]")
    except NoSuchElementException:
        pass
    return el


'''
    Кнопка найти новостройки
'''
def get_but_more(driver: webdriver.Chrome):
    el = None
    try:
        el = driver.find_element(By.XPATH, "//button[@id='loadmore']")
    except NoSuchElementException:
        pass
    return el


def set_driver_options(options):
    # безголовый режим браузера
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-setuid-sandbox')

    # options.add_argument("--disable-extensions")  # Отключить расширения
    options.add_argument("--disable-plugins")  # Отключить плагины
    options.add_argument("--disable-internal-tmp-true")  # Включить сжатие временных файлов

    # options.add_argument('--headless=new')
    # options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument('--disable-accelerated-2d-canvas')
    # options.add_argument("--disable-font-antialiasing")
    options.add_argument("--disable-preconnect")
    # options.add_argument("--disk-cache-size=0")
    options.add_argument('--disable-infobars')
    # options.add_argument('--disable-notifications')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl- errors')
    options.add_argument('--disable-blink-features=AutomationControlled')
    # prefs = {
    #     'profile.managed_default_content_settings.images': 2,
    #     'css.animations': False
    # }
    # options.add_experimental_option("prefs", prefs)


def get_selenium_driver(use_proxy, mobile_mode):
    options = webdriver.ChromeOptions()
    set_driver_options(options)

    if use_proxy:
        set_proxy(options)

    if mobile_mode:
        mobile_emulation = {'deviceName': f'{random.choice(mob_devices)}'}
        options.add_experimental_option('mobileEmulation', mobile_emulation)
    else:
        ua = UserAgent()
        options.add_argument(f'--user-agent={ua.random}')

    caps = DesiredCapabilities().CHROME
    caps['pageLoadStrategy'] = 'normal'

    service = Service('./web_driver/chromedriver', desired_capabilities=caps)
    driver = webdriver.Chrome(service=service, options=options)

    return driver


mob_devices = [
    "Apple iPhone 3GS",
    "Apple iPhone 4",
    "Apple iPhone 5",
    "Apple iPhone 6",
    "Apple iPhone 6 Plus",
    "BlackBerry Z10",
    "BlackBerry Z30",
    "Google Nexus 4",
    "Google Nexus 5",
    "Google Nexus S",
    "HTC Evo, Touch HD, Desire HD, Desire",
    "HTC One X, EVO LTE",
    "HTC Sensation, Evo 3D",
    "LG Optimus 2X, Optimus 3D, Optimus Black",
    "LG Optimus G",
    "LG Optimus LTE, Optimus 4X HD",
    "LG Optimus One",
    "Motorola Defy, Droid, Droid X, Milestone",
    "Motorola Droid 3, Droid 4, Droid Razr, Atrix 4G, Atrix 2",
    "Motorola Droid Razr HD",
    "Nokia C5, C6, C7, N97, N8, X7",
    "Nokia Lumia 7X0, Lumia 8XX, Lumia 900, N800, N810, N900",
    "Samsung Galaxy Note 3",
    "Samsung Galaxy Note II",
    "Samsung Galaxy Note",
    "Samsung Galaxy S III, Galaxy Nexus",
    "Samsung Galaxy S, S II, W",
    "Samsung Galaxy S4",
    "Sony Xperia S, Ion",
    "Sony Xperia Sola, U",
    "Sony Xperia Z, Z1",
    "Amazon Kindle Fire HDX 7″",
    "Amazon Kindle Fire HDX 8.9″",
    "Amazon Kindle Fire (First Generation)",
    "Apple iPad 1 / 2 / iPad Mini",
    "Apple iPad 3 / 4",
    "BlackBerry PlayBook",
    "Google Nexus 10",
    "Google Nexus 7 2",
    "Google Nexus 7",
    "Motorola Xoom, Xyboard",
    "Samsung Galaxy Tab 7.7, 8.9, 10.1",
    "Samsung Galaxy Tab",
    "Notebook with touch"
]

links = [
    'https://www.novostroyki-spb.ru/rejting-stroitelnyh-kompanij-sankt-peterburga',
    'https://www.novostroyki-spb.ru/novostroyki-ekonom-klassa',
    'https://www.novostroyki-spb.ru/novosti',
    'https://www.novostroyki-spb.ru/skidki-na-kvartiry',
    'https://www.novostroyki-spb.ru/',
    'https://www.novostroyki-spb.ru/agreement',
    'https://www.novostroyki-spb.ru/privacy-policy'
]


def set_proxy(options):
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    plugin_file = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(plugin_file, 'w') as zp:
        zp.writestr('manifest.json', secure.get_proxy_pref(0))
        zp.writestr('background.js', secure.get_proxy_pref(1))
    options.add_extension(plugin_file)


def start_selen():
    driver = get_selenium_driver(True, True)
    driver.get(url)
    time.sleep(10)
    pass


def change_proxy():
    if secure.PROXY_ID < secure.num_proxs - 1:
        secure.PROXY_ID += 1
    else:
        secure.PROXY_ID = 0
