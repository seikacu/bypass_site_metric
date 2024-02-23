import random
import time
import traceback

import numpy as np
import scipy.interpolate as si

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from check_visible import is_visible
from move_mouse import mouse_move_to_element
from scrolling_ import scroll
from utils import get_location_characteristics
from utils import get_window_characteristics

import secure

TIME_SLEEP = 0.05
MAX_STEP = 20
MAX_STEP2 = random.randint(30, 35)

mls_01_1 = [
    0.1,
    0.2,
    0.3,
    0.4,
    0.5,
    0.6,
    0.7,
    0.8,
    0.9,
    1.0
]


mls = [
    0.2,
    0.4,
    0.6,
    0.8,
    1.0
]


mls_05 = [
    0.1,
    0.2,
    0.3,
    0.4,
    0.5
]

mls_03 = [
    0.1,
    0.2,
    0.3
]
TIME_SLEEP2 = random.choice(mls_03)


mls_06_1 = [
    0.5,
    0.6,
    0.7,
    0.8,
    0.9,
    1.0
]


# time_read_news = random.randrange(30, 45)
time_read_news = random.randrange(15, 30)
time_delay = random.randrange(3, 7)
time_mls = random.choice(mls)
time_mls_05 = random.choice(mls_05)
time_mls_06_1 = random.choice(mls_06_1)


def scroll_move_click_pc_2(action: ActionChains, driver: webdriver.Chrome, el: WebElement, mouse):
    while not is_visible(driver, el):
        offset = 0
        STEP = random.randint(10, MAX_STEP)
        elem_top_bound, elem_lower_bound = get_location_characteristics(el)
        win_upper_bound, win_lower_bound = get_window_characteristics(
            driver)
        while elem_lower_bound < win_upper_bound:
            offset = -1
            elem_top_bound, elem_lower_bound = get_location_characteristics(el)
            win_upper_bound, win_lower_bound = get_window_characteristics(
                driver)
            elem_top_bound, elem_lower_bound = get_location_characteristics(el)
            scroll(driver, -STEP)
            time.sleep(TIME_SLEEP)
            # else:
            #     scroll(driver, -STEP)
        while elem_top_bound > win_lower_bound:
            offset = 1
            # page_y_offset = driver.execute_script('return window.pageYOffset;')
            elem_top_bound, elem_lower_bound = get_location_characteristics(
                el)
            win_upper_bound, win_lower_bound = get_window_characteristics(
                driver)
            scroll(driver, STEP)
            time.sleep(TIME_SLEEP)
            # else:
            #     scroll(driver, STEP)
            # clas = el.get_attribute("class")
            # if clas == "carousel__slide is-selected":
            #     break
        if offset == -1:
            for _ in range(0, MAX_STEP2):
                scroll(driver, -STEP)
                time.sleep(TIME_SLEEP2)
        elif offset == 1:
            for _ in range(0, MAX_STEP2):
                scroll(driver, STEP)
                time.sleep(TIME_SLEEP2)

    # action.move_to_element(el).click().perform()
    # mouse_click(action)
    # except Exception:
    #     pass
    # finally:


def scroll_move_click_pc(action: ActionChains, driver: webdriver.Chrome, el: WebElement, mouse):
    STEP = random.randint(10, MAX_STEP)
    offset = int(driver.get_window_size()['height'])
    page_y_offset = driver.execute_script('return window.pageYOffset;')
    offset += page_y_offset
    delta_y = int(el.rect['y'])
    el_height = int(el.rect['height'])
    if delta_y < page_y_offset:
        while delta_y - 200 < page_y_offset:
            scroll(driver, -STEP)
            time.sleep(TIME_SLEEP)
            page_y_offset -= STEP
    else:
        print(f"el_height - {el_height}")
        while offset < delta_y + 400:
            scroll(driver, STEP)
            time.sleep(TIME_SLEEP)
            offset += STEP
    # time.sleep(random.choice(mls_01_1))
    # mouse_move_to_element(action, driver, mouse, el)
    # time.sleep(time_mls_05)
    # ActionChains(driver).move_to_element(el).click().perform()
    # action.move_to_element(el)
    # time.sleep(time_mls_05)
    # ActionChains(driver).click().perform()


# def scroll_move_click_pc(action: ActionChains, driver: webdriver.Chrome, el: WebElement, mouse):
#     offset = int(driver.get_window_size()['height'])
#     page_y_offset = driver.execute_script('return window.pageYOffset;')
#     offset += page_y_offset
#     delta_y = int(el.rect['y'])
#     win_upper_bound, win_lower_bound = get_window_characteristics(driver)
#     if delta_y < page_y_offset:
#         while delta_y < page_y_offset:
#             count = random.randrange(-100, 0)
#             action.scroll_by_amount(0, count).perform()
#             time.sleep(time_mls)
#             page_y_offset += count
#         time.sleep(time_delay)

#         mouse_move_to_element(driver, mouse, el)
#         # move_mouse(driver, el)
#         # move_to_element(driver, el)
#         time.sleep(time_mls)
#         action.click(el).perform()
#     else:
#         while offset < delta_y + 200:
#             count = 0
#             if delta_y > 0 and delta_y >= 100:
#                 count = random.randrange(0, 100)
#             elif delta_y < 0 and delta_y <= -100:
#                 count = random.randrange(-100, 0)
#             elif 0 < delta_y < 100:
#                 count = delta_y
#             elif 0 > delta_y > -100:
#                 count = delta_y
#             action.scroll_by_amount(0, count).perform()
#             time.sleep(time_mls)
#             offset += count
#         time.sleep(time_delay)
#         mouse_move_to_element(driver, mouse, el)
#         # move_mouse(action, el)
#         # move_to_element(driver, el)
#         time.sleep(time_mls)
#         action.click(el).perform()


def scroll_down_screen(action: ActionChains, driver: webdriver.Chrome, height_end_page: int):
    time.sleep(time_read_news)
    offset = int(driver.get_window_size()['height'])
    stop = random.randint(5, 10)
    start = 0
    while offset <= height_end_page:
        if start == stop:
            start = 0
            time.sleep(time_read_news)
        count = random.randrange(0, 100)
        action.scroll_by_amount(0, count).perform()
        time.sleep(time_mls)
        offset += count
        start += 1
    if offset >= height_end_page:
        time.sleep(time_read_news)


def move_touch(action: ActionChains, el: WebElement):
    action.pointer_action.move_to(el).pointer_down().move_by(2, 2)
    action.perform()
    time.sleep(time_mls)
    action.pointer_action.move_to(el).pointer_down().pointer_up()
    action.perform()


def touch(action: ActionBuilder, el: WebElement):
    action.pointer_action\
        .move_to(el)\
        .pointer_down()\
        .move_by(2, 2)\
        .pointer_up()
    action.perform()


def move(action: ActionBuilder):
    action.pointer_action.move_to_location(0, 800).pointer_down().move_by(
        2, 2, tilt_x=-72, tilt_y=9, twist=86).pointer_up(1)
    action.perform()


def select_by_ref_pc(driver: webdriver.Chrome) -> WebElement:
    li = None
    try:
        nav = driver.find_element(
            By.XPATH, "//nav[contains(@class, 'nav-desktop')]")
        lis = nav.find_elements(By.TAG_NAME, 'li')
        random.shuffle(lis)
        li = random.choice(lis)
        # li = lis[0]
    except NoSuchElementException:
        secure.log.write_log('traceback', traceback.format_exc())
    return li


def get_main_but_mob(driver: webdriver.Chrome) -> WebElement:
    nav_btn = None
    try:
        nav_btn = driver.find_element(
            By.XPATH, "//label[contains(@class, 'nav-btn__label')]")
    except NoSuchElementException:
        secure.log.write_log('traceback', traceback.format_exc())
    return nav_btn


def select_by_ref_mob(driver: webdriver.Chrome) -> WebElement:
    li = None
    try:
        nav = driver.find_element(
            By.XPATH, "//nav[contains(@class, 'nav-mobile')]")
        lis = nav.find_elements(By.TAG_NAME, 'li')
        random.shuffle(lis)
        li = random.choice(lis)
        # li = lis[0]
    except NoSuchElementException:
        secure.log.write_log('traceback', traceback.format_exc())
    return li


# Строка поиска новостроек
def get_find_box(driver: webdriver.Chrome) -> WebElement:
    el = None
    try:
        el = driver.find_element(
            By.XPATH, "//input[@placeholder='Поиск новостроек']")
    except NoSuchElementException:
        secure.log.write_log('traceback', traceback.format_exc())
    return el


# Кнопка найти новостройки
def get_but_find(driver: webdriver.Chrome) -> WebElement:
    el = None
    try:
        el = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Найти')]")
    except NoSuchElementException:
        secure.log.write_log('traceback', traceback.format_exc())
    return el


# Кнопка "Найти еще" / "Показать еще"
def get_but_more(driver: webdriver.Chrome) -> WebElement:
    el = None
    try:
        el = driver.find_element(By.XPATH, "//button[@id='loadmore']")
    except NoSuchElementException:
        secure.log.write_log('traceback', traceback.format_exc())
    return el


# Кнопка закрыть всплывающее окно
def get_x_but(driver: webdriver.Chrome) -> WebElement:
    el = None
    try:
        el = driver.find_element(
            By.XPATH, "//a[@id='everystraus_callback_close']")
    except NoSuchElementException:
        secure.log.write_log('traceback', traceback.format_exc())
    return el


# Кнопка позвонить
def get_call_but(driver: webdriver.Chrome) -> WebElement:
    el = None
    try:
        el = driver.find_element(
            By.XPATH, "//div[@id='everystraus_callback_phone']")
    except NoSuchElementException:
        secure.log.write_log('traceback', traceback.format_exc())
    return el


def scroll_down_yoffset(driver: webdriver.Chrome, element: WebElement, y: int):
    ActionChains(driver).move_to_element_with_offset(element, 0, y).perform()


def get_min_max_top(driver: webdriver.Chrome) -> WebElement:
    punkts = driver.find_elements(By.XPATH, "//div[contains(@class, 'punkt')]")
    punkt = random.choice(punkts)
    parent = punkt.find_element(By.XPATH, "..")
    return parent


def rand_tap_but_more(action: ActionBuilder, but_more: WebElement, driver: webdriver.Chrome):
    scrols = random.randrange(1, 10)
    for i in range(0, scrols):
        if but_more is None:
            break
        time.sleep(time_delay)
        move_touch(action, but_more)
        time.sleep(time_delay)
        but_more = get_but_more(driver)
        i += 1


def change_developer(action: ActionChains, driver: webdriver.Chrome):
    table = driver.find_elements(By.TAG_NAME, 'tr')
    random.shuffle(table)
    developer = random.choice(table)
    href = developer.find_element(By.TAG_NAME, 'a')
    move_touch(action, href)


def get_pictures(driver: webdriver.Chrome) -> WebElement:
    el = None
    try:
        try:
            el = driver.find_element(
                By.XPATH, '//div[contains(@class, "thumb-gallery__fullscreen gallery__fullscreen_new_top")]')
        except NoSuchElementException:
            pass
        if el is None:
            el = driver.find_element(
                By.XPATH, '//div[contains(@class, "carousel__slide is-selected")]')
    except NoSuchElementException:
        secure.log.write_log('traceback', traceback.format_exc())
    return el


def get_pictures_progres(driver: webdriver.Chrome):
    el = None
    try:
        try:
            els = driver.find_elements(
                By.XPATH, '//div[contains(@class, "thumb-gallery__fullscreen gallery__fullscreen_new")]')
        except NoSuchElementException:
            pass
        if els is None:
            els = driver.find_elements(
                By.XPATH, '//div[contains(@class, "carousel__slide is-selected")]')
        if len(els) < 2:
            return el
        elif len(els) == 2:
            return els[1]
    except NoSuchElementException:
        secure.log.write_log('traceback', traceback.format_exc())


# Кнопка запустить слайдшоу
def get_slideshow_but(driver: webdriver.Chrome) -> WebElement:
    el = None
    try:
        el = driver.find_element(
            By.XPATH, '//button[contains(@class, "button--slideshow")]')
    except NoSuchElementException:
        secure.log.write_log('traceback', traceback.format_exc())
    return el


def get_slideshow_close(driver: webdriver.Chrome) -> WebElement:
    el = None
    try:
        el = driver.find_element(
            By.XPATH, '//button[contains(@class, "fancybox__button--close")]')
    except NoSuchElementException:
        secure.log.write_log('traceback', traceback.format_exc())
    return el


# РАЗДЕЛ - Все новостройки СПб
def get_hrefs_zhk(driver: webdriver.Chrome) -> list:
    links = []
    hrefs = driver.find_elements(By.XPATH, "//a[contains(@href,'/zhk-')]")
    for href in hrefs:
        links.append(href.get_attribute("href"))
    return links


# РАЗДЕЛ - Новостройки по районам
def get_hrefs_novostrojki(driver: webdriver.Chrome) -> list:
    links = []
    hrefs = driver.find_elements(
        By.XPATH, "//a[contains(@href,'/novostrojki-')]")
    for href in hrefs:
        links.append(href.get_attribute("href"))
    return links


# РАЗДЕЛ - Новостройки у метро
def get_hrefs_metro(driver: webdriver.Chrome) -> list:
    links = []
    hrefs = driver.find_elements(By.XPATH, "//a[contains(@href,'/metro-')]")
    for href in hrefs:
        links.append(href.get_attribute("href"))
    return links


def get_cads_links(driver: webdriver.Chrome) -> list:
    cards_links = driver.find_elements(
        By.XPATH, "//li[contains(@class,'card-list__item')]")
    hrefs = []
    for card in cards_links:
        tag_a = card.find_element(By.TAG_NAME, "a")
        href = tag_a.get_attribute('href')
        hrefs.append(href)
    return hrefs


def get_click_but_more(action: ActionChains, driver: webdriver.Chrome):
    but_more = get_but_more(driver)
    if but_more is not None:
        time.sleep(time_delay)
        move_touch(action, but_more)
        time.sleep(time_delay)


# Получить элемент для перехода по ссылке
def get_element_by_href(driver: webdriver, href: str) -> WebElement:
    return driver.find_element(By.XPATH, f"//a[contains(@href,'{href}')]")


def get_count_img(driver: webdriver.Chrome) -> int:
    img_count = driver.find_element(By.XPATH, "//span[@data-fancybox-count]")
    return int(img_count.text)


# Развернуть список главного элемента
def get_but_main_el_select(driver: webdriver, el: str) -> WebElement:
    links_btns = driver.find_elements(
        By.XPATH, "//span[contains(@class,'links__btn')]")
    if el == 'metro':
        print("Метро")
        return links_btns[0]
    elif el == 'novostrojki':
        print("Новостройки по районам")
        return links_btns[1]
    elif el == 'zhk':
        print("Все новостройки СПб")
        return links_btns[2]
    else:
        print("Портал о новостройках Санкт-Петербурга")
        return links_btns[3]


func_main = [
    get_hrefs_metro,
    get_hrefs_novostrojki,
    get_hrefs_zhk
]

random.shuffle(func_main)
random_func_main = random.choice(func_main)


news_mode = [
    get_cads_links,
]


def get_read_docs(driver: webdriver.Chrome) -> WebElement:
    el = None
    hrefs = ["/agreement", "/privacy-policy"]
    href = random.choice(hrefs)
    try:
        el = get_element_by_href(driver, href)
    except NoSuchElementException:
        secure.log.write_log('traceback', traceback.format_exc())
    return el


# Прокрутить колесо мыши до элемента
def move_to_element(driver: webdriver, el: WebElement):
    # ActionChains(driver).w3c_actions.pointer_action.move_to_location(100, 100)
    ActionChains(driver).move_to_element(el).pause(time_mls).perform()


# Получить координаты элемента
def get_el_location(el: WebElement) -> dict:
    return el.location


def scroll_down_page(driver: webdriver.Chrome, speed=25):
    current_scroll_position, new_height = 0, 1
    while current_scroll_position <= new_height:
        # time.sleep(random.choice(mls))
        current_scroll_position += speed
        driver.execute_script(
            "window.scrollTo(0, {});".format(current_scroll_position))
        new_height = driver.execute_script("return document.body.scrollHeight")


def scroll_down_to_element(driver: webdriver.Chrome, y: int, speed=100):
    current_scroll_position, new_height = 0, 1
    while current_scroll_position <= new_height:
        time.sleep(random.choice(mls))
        current_scroll_position += speed
        driver.execute_script(
            "window.scrollTo(0, {});".format(current_scroll_position))
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height >= y:
            break


def scrooll_down(actions):
    for _ in range(5):
        actions.send_keys(Keys.ARROW_DOWN)
        actions.perform()
        time.sleep(random.choice(mls_05))


def smoth_scrool(driver: webdriver.Chrome, el: WebElement):
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", el)


def scroll_to_el(action: ActionChains, el: WebElement):
    action.pause(time_mls).move_to_element(el).pause(time_mls)


def _in_viewport(driver: webdriver.Chrome, el: WebElement):
    script = (
        "for(var e=arguments[0],f=e.offsetTop,t=e.offsetLeft,o=e.offsetWidth,n=e.offsetHeight;\n"
        "e.offsetParent;)f+=(e=e.offsetParent).offsetTop,t+=e.offsetLeft;\n"
        "return f<window.pageYOffset+window.innerHeight&&t<window.pageXOffset+window.innerWidth&&f+n>\n"
        "window.pageYOffset&&t+o>window.pageXOffset"
    )
    return driver.execute_script(script, el)


def check_dialog_class(driver: webdriver.Chrome, mode: str, mouse):
    try:
        iframe = driver.find_element(
            By.XPATH, "//div[@id='everystraus_add_blur']")
        if iframe.get_attribute("style") == "display: block;":
            but_x = get_x_but(driver)
            if mode == 'PC':
                action = ActionChains(driver)
                # mouse = Mouse()
                mouse_move_to_element(action, driver, mouse, but_x)
                # move_mouse(driver, but_x)
                # move_to_element(driver, but_x)
                # time.sleep(time_mls)
                action.click(but_x).perform()
            elif mode == 'mobile':
                touch_input = PointerInput(POINTER_TOUCH, "touch")
                action = ActionBuilder(driver, mouse=touch_input)

                action.pointer_action.move_to(
                    but_x).pointer_down().move_by(2, 2)
                action.perform()
                time.sleep(time_mls)
                action.pointer_action.move_to(
                    but_x).pointer_down().pointer_up()
                action.perform()
    except:
        pass


def interpolate_move() -> list:
    # Curve base:
    points = [[0, 0], [0, 2], [2, 3], [4, 0], [6, 3], [8, 2], [8, 0]]
    points = np.array(points)

    x = points[:, 0]
    y = points[:, 1]

    t = range(len(points))
    ipl_t = np.linspace(0.0, len(points) - 1, 100)

    x_tup = si.splrep(t, x, k=3)
    y_tup = si.splrep(t, y, k=3)

    x_list = list(x_tup)
    xl = x.tolist()
    x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

    y_list = list(y_tup)
    yl = y.tolist()
    y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

    x_i = si.splev(ipl_t, x_list)  # x interpolate values
    y_i = si.splev(ipl_t, y_list)  # y interpolate values
    return [x_i, y_i]


def move_mouse(action: ActionChains, el: WebElement):
    # First, go to your start point or Element:
    # action.move_to_element(start_element)
    # action.perform()

    for mouse_x, mouse_y in zip(interpolate_move()[0], interpolate_move()[1]):
        action.move_to_element_with_offset(el, mouse_x, mouse_y)
        action.perform()
        print(mouse_x, mouse_y)
        secure.log.write_log('move_mouse', f'{mouse_x}, {mouse_y}')


def properties(element) -> dict:
    kv = element.text.split(' ', 1)[1].split(', ')
    return {x[0]: x[1] for x in list(map(lambda item: item.split(': '), kv))}


# Функция для выполнения проверки в отдельном потоке
def check_dialog_thread(stop: bool, driver: webdriver.Chrome, mode: str, mouse):
    while True:
        check_dialog_class(driver, mode, mouse)
        if stop():
            break


# class ActionChainsChild(ActionChains):
#     def move_by_offset(self, xoffset, yoffset):
#         if self._driver.w3c:
#             self.w3c_actions.pointer_action.move_by(xoffset, yoffset)
#             # self.w3c_actions.key_action.pause()
#         else:
#             self._actions.append(lambda: self._driver.execute(
#                 Command.MOVE_TO, {
#                     'xoffset': int(xoffset),
#                     'yoffset': int(yoffset)}))
#         return self
