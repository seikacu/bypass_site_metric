import platform
import random
import zipfile

from fake_useragent import UserAgent
from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service

import secure


def get_path_webdriver() -> str:
    if platform.system() == "Windows":
        return r".\web_driver\chromedriver.exe"
    elif platform.system() == "Linux":
        return "./web_driver/chromedriver"
    elif platform.system() == "Darwin":
        return "./web_driver/chromedriver-macos"
    else:
        raise Exception("Unsupported platform!")


def set_driver_options(options):
    options.binary_location = "/usr/bin/chromium"
    # options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument('--headless=new')
    options.add_argument("--no-sandbox")
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2,
    })
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-notifications')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--disable-blink-features=AutomationControlled')


def get_selenium_driver(use_proxy, mode):
    options = webdriver.ChromeOptions()
    set_driver_options(options)

    if use_proxy:
        set_proxy(options)

    if mode == 'mobile':
        mobile_emulation = {'deviceName': f'{random.choice(mob_devices)}'}
        # mobile_emulation = {'deviceName': 'Samsung Galaxy S22+'}
        options.add_experimental_option('mobileEmulation', mobile_emulation)
        secure.log.write_log('mobile', mobile_emulation)
        print(mobile_emulation)
        driver = webdriver.Chrome(options=options)
    elif mode == 'PC':
        ua = UserAgent()
        fake_browser = ua.random
        secure.log.write_log('PC', fake_browser)
        print(fake_browser)
        options.add_argument(f'--user-agent={fake_browser}')
        caps = DesiredCapabilities().CHROME

        caps['pageLoadStrategy'] = 'normal'
        service = Service(get_path_webdriver(), desired_capabilities=caps)
        driver = webdriver.Chrome(service=service, options=options)
        width = random.randint(900, 1920)
        height = random.randint(900, 1400)
        driver.set_window_size(width, height)

    return driver


mob_devices = [
    'iPhone XR',
    'iPhone 6',
    'iPhone 6 Plus',
    'iPhone 14 Pro Max',
    'iPhone 12 Pro',
    'Pixel 3 XL',
    'BlackBerry Z30',
    'Galaxy Note 3',
    'Galaxy Note II',
    'Galaxy S III',
    'Galaxy S8',
    'Galaxy S9+',
    'Galaxy Tab S4',
    'Kindle Fire HDX',
    'LG Optimus L70',
    'Microsoft Lumia 550',
    'Microsoft Lumia 950',
    'Moto G Power',
    'Moto G4',
    'Nexus 10',
    'Nexus 4',
    'Nexus 5',
    'Nexus 5X',
    'Nexus 6',
    'Nexus 6P',
    'Nexus 7',
    'Nexus 10',
    'Nokia N9',
    'Pixel 3',
    'Pixel 4',
    'Pixel 7',
    'Samsung Galaxy S8+',
    'Samsung Galaxy S20 Ultra',
    'iPad Mini',
    'iPad Air',
    'Surface Duo',
    'Samsung Galaxy A51/71',
    'Galaxy S5',
    'Pixel 2',
    'Pixel 2 XL',
    'iPhone 6/7/8',
    'iPhone 6/7/8 Plus',
    'iPhone X',
    'iPad',
    'Facebook on Android'
]


# everystraus_ref = [
#     'https://yandex.ru/'
# ]


def get_coordinates(location):
    geolocator = Nominatim(user_agent="geo_locator")
    location = geolocator.geocode(location)
    return location.latitude, location.longitude


def set_proxy(options):
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    plugin_file = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(plugin_file, 'w') as zp:
        zp.writestr('manifest.json', secure.get_proxy_pref(0))
        zp.writestr('background.js', secure.get_proxy_pref(1))
    options.add_extension(plugin_file)


# def set_proxy(options):
#     # options.add_experimental_option('excludeSwitches', ['enable-logging'])
#     options.add_experimental_option('excludeSwitches', [
#         'enable-automation',
#         "disable-background-networking",
#         "disable-client-side-phishing-detection",
#         "disable-default-apps",
#         "disable-hang-monitor",
#         "disable-popup-blocking",
#         "disable-prompt-on-repost",
#         "enable-blink-features=ShadowDOMV0",
#         "enable-logging",
#         "force-fieldtrials=SiteIsolationExtensions/Control",
#         # "load-extension=/var/folders/zz/zyxvpxvq6csfxvn_n0001_y8000_qk/T/.com.google.Chrome.HPBfiz/internal",
#         "log-level=0",
#         # "password-store=basic",
#         # "remote-debugging-port=0",
#         # "test-type=webdriver",
#         "use-mock-keychain",
#     ])
#     options.add_experimental_option('useAutomationExtension', False)
#     # print(f'--proxy-server={secure.proxies[secure.PROXY_ID]}')
#     # options.add_argument(f'--proxy-server={secure.proxies[secure.PROXY_ID]}')
#     # PROXY = '134.209.29.120:3128'
#     # options.add_argument(f'--proxy-server=%s' % PROXY)


# plugin_file = 'proxy_auth_plugin.zip'
# with zipfile.ZipFile(plugin_file, 'w') as zp:
#     zp.writestr('manifest.json', secure.get_proxy_pref(0))
#     zp.writestr('background.js', secure.get_proxy_pref(1))
# options.add_extension(plugin_file)


def change_proxy():
    if secure.PROXY_ID < secure.num_proxs - 1:
        secure.PROXY_ID += 1
    else:
        secure.PROXY_ID = 0
