import random
import time

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

import secure

stop_threads = False


mls = [
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


time_delay = random.randrange(1, 5)
time_mls = random.choice(mls)


def scroll_move_click_pc(action, driver: webdriver.Chrome, el):
    offset = int(driver.get_window_size()['height'])
    page_y_offset = driver.execute_script('return window.pageYOffset;')
    offset += page_y_offset
    delta_y = int(el.rect['y'])
    if delta_y < page_y_offset:
        print('Двигаем назад!!!')
        secure.log.write_log('scroll_move_click_pc', 'Нужно настроить сколлинг назад!!!')
    while offset < delta_y + 200:
        count = 0
        if delta_y > 0 and delta_y >= 100:
            count = random.randrange(0, 100)
        elif delta_y < 0 and delta_y <= -100:
            count = random.randrange(-100, 0)
        # elif (0 < y < 100) or (0 > y > -100):
        elif 0 < delta_y < 100:
            count = delta_y
            move_mouse(action)
        elif 0 > delta_y > -100:
            count = delta_y
        # elif 0 > y > -100:
        #     count = y
        # if count >= 100 or count <= -100:
        action.scroll_by_amount(0, count).perform()
        time.sleep(time_mls)  # Adjust sleep duration as needed
        offset += count
    # action.scroll_to_element(el).pause(time_mls).perform()
    time.sleep(time_delay)
    # driver.save_screenshot("screenshots/screenshot_00.png")
    move_to_element(driver, el)
    # move_mouse(action)
    time.sleep(time_mls)
    action.click(el).perform()


def scroll_down_screen(action, driver: webdriver.Chrome, el):
    page_y_offset = driver.execute_script('return window.pageYOffset;')
    offset += page_y_offset
    delta_y = int(el.rect['y'])
    if delta_y < page_y_offset:
        print('Двигаем назад!!!')
        secure.log.write_log('scroll_move_click_pc', 'Нужно настроить сколлинг назад!!!')
    while offset < delta_y + 200:
        count = 0
        if delta_y > 0 and delta_y >= 100:
            count = random.randrange(0, 100)
        elif delta_y < 0 and delta_y <= -100:
            count = random.randrange(-100, 0)
        # elif (0 < y < 100) or (0 > y > -100):
        elif 0 < delta_y < 100:
            count = delta_y
            move_mouse(action)
        elif 0 > delta_y > -100:
            count = delta_y
        # elif 0 > y > -100:
        #     count = y
        # if count >= 100 or count <= -100:
        action.scroll_by_amount(0, count).perform()
        time.sleep(time_mls)  # Adjust sleep duration as needed
        offset += count
    # action.scroll_to_element(el).pause(time_mls).perform()
    time.sleep(time_delay)
    # driver.save_screenshot("screenshots/screenshot_00.png")
    move_to_element(driver, el)
    # move_mouse(action)
    time.sleep(time_mls)
    action.click(el).perform()


def move_touch(action, driver, el):
    action.pointer_action.move_to(el).pointer_down().move_by(2, 2)
    action.perform()
    time.sleep(time_mls)
    driver.save_screenshot("screenshots/screenshot_01.png")
    action.pointer_action.move_to(el).pointer_down().pointer_up()
    action.perform()


def select_by_ref_pc(driver: webdriver.Chrome):
    li = None
    try:
        nav = driver.find_element(By.XPATH, "//nav[contains(@class, 'nav-desktop')]")
        lis = nav.find_elements(By.TAG_NAME, 'li')
        # li = random.choice(lis)
        li = lis[2]
    except NoSuchElementException:
        pass
    return li


def select_by_ref_mob(action, driver: webdriver.Chrome):
    li = None
    try:
        nav_btn = driver.find_element(By.XPATH, "//label[contains(@class, 'nav-btn__label')]")
        move_touch(action, driver, nav_btn)
        time.sleep(time_delay)
        nav = driver.find_element(By.XPATH, "//nav[contains(@class, 'nav-mobile')]")
        lis = nav.find_elements(By.TAG_NAME, 'li')
        li = random.choice(lis)
        # li = lis[5]
    except NoSuchElementException:
        pass
    return li


''' Строка поиска новостроек '''


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
    Кнопка "Найти еще" / "Показать еще"
'''


def get_but_more(driver: webdriver.Chrome):
    el = None
    try:
        el = driver.find_element(By.XPATH, "//button[@id='loadmore']")
    except NoSuchElementException:
        pass
    return el


'''
    Кнопка закрыть всплывающее окно
'''


def get_x_but(driver: webdriver.Chrome):
    el = None
    try:
        el = driver.find_element(By.XPATH, "//a[@id='everystraus_callback_close']")
    except NoSuchElementException:
        pass
    return el


'''
    Кнопка позвонить
'''


def get_call_but(driver: webdriver.Chrome):
    el = None
    try:
        el = driver.find_element(By.XPATH, "//div[@id='everystraus_callback_phone']")
    except NoSuchElementException:
        pass
    return el


def scroll_down_yoffset(driver: webdriver.Chrome, element: WebElement, y):
    ActionChains(driver).move_to_element_with_offset(element, 0, y).perform()


'''
    Вернуть рандомную ссылку на квартиры в наличии или документы застройщика
'''

'''
    Открыть просмотр картинок по застройщику
'''


def get_pictures(driver: webdriver.Chrome):
    el = None
    try:
        el = driver.find_element(By.XPATH, '//div[contains(@class, "carousel__slide is-selected")]')
    except NoSuchElementException:
        pass
    return el


def get_pictures_progres(driver: webdriver.Chrome):
    el = None
    try:
        els = driver.find_elements(By.XPATH, '//div[contains(@class, "carousel__slide is-selected")]')
        if len(els) < 2:
            return el
        elif len(els) == 2:
            return els[1]
    except NoSuchElementException:
        pass


'''
    Найти кнопку запустить слайдшоу 
'''


def get_slideshow_but(driver: webdriver.Chrome):
    el = None
    try:
        el = driver.find_element(By.XPATH, '//button[contains(@class, "button--slideshow")]')
    except NoSuchElementException:
        pass
    return el


def get_slideshow_close(driver: webdriver.Chrome):
    el = None
    try:
        el = driver.find_element(By.XPATH, '//button[contains(@class, "fancybox__button--close")]')
    except NoSuchElementException:
        pass
    return el


""" Все новостройки СПб """


def get_hrefs_zhk(driver: webdriver.Chrome):
    links = []
    hrefs = driver.find_elements(By.XPATH, "//a[contains(@href,'/zhk-')]")
    for href in hrefs:
        links.append(href.get_attribute("href"))
    return links


""" Новостройки по районам """


def get_hrefs_novostrojki(driver: webdriver.Chrome):
    links = []
    hrefs = driver.find_elements(By.XPATH, "//a[contains(@href,'/novostrojki-')]")
    for href in hrefs:
        links.append(href.get_attribute("href"))
    return links


""" Новостройки у метро """


def get_hrefs_metro(driver: webdriver.Chrome):
    links = []
    hrefs = driver.find_elements(By.XPATH, "//a[contains(@href,'/metro-')]")
    for href in hrefs:
        links.append(href.get_attribute("href"))
    return links


def get_cads_links(driver):
    cards_links = driver.find_elements(By.XPATH, "//li[contains(@class,'card-list__item')]")
    hrefs = []
    for card in cards_links:
        tag_a = card.find_element(By.TAG_NAME, "a")
        href = tag_a.get_attribute('href')
        hrefs.append(href)
    return hrefs


def get_click_but_more(action, driver):
    but_more = get_but_more(driver)
    if but_more is None:
        time.sleep(time_delay)
        move_touch(action, driver, but_more)
        time.sleep(time_delay)


''' Получить элемент для перехода по ссылке '''


def get_element_by_href(driver: webdriver, href):
    return driver.find_element(By.XPATH, f"//a[contains(@href,'{href}')]")


''' Развернуть список главного элемента '''


def get_but_main_el_select(driver: webdriver, main_el_select):
    links_btns = driver.find_elements(By.XPATH, f"//span[contains(@class,'links__btn')]")
    if main_el_select == 'metro':
        return links_btns[0]
    elif main_el_select == 'novostrojki':
        return links_btns[1]
    elif main_el_select == 'zhk':
        return links_btns[2]
    else:
        return links_btns[3]


func_main = [
    get_hrefs_metro,
    get_hrefs_novostrojki,
    get_hrefs_zhk
]

random_func_main = random.choice(func_main)


news_mode = [
    get_cads_links,
]


# Прокрутить колесо мыши до элемента
def move_to_element(driver: webdriver, element):
    ActionChains(driver).move_to_element(element).pause(time_mls).perform()


'''
    Получить координаты элемента
'''


def get_el_location(el: WebElement):
    return el.location


mls = [
    0.2,
    0.4,
    0.6,
    0.8,
    1.0
]


def scroll_down_page(driver, speed=100):
    current_scroll_position, new_height = 0, 1
    while current_scroll_position <= new_height:
        time.sleep(random.choice(mls))
        current_scroll_position += speed
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        new_height = driver.execute_script("return document.body.scrollHeight")


def scroll_down_to_element(driver, y, speed=100):
    current_scroll_position, new_height = 0, 1
    while current_scroll_position <= new_height:
        time.sleep(random.choice(mls))
        current_scroll_position += speed
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height >= y:
            break


mls_05 = [
    0.1,
    0.2,
    0.3,
    0.4,
    0.5
]


def scrooll_down(actions):
    for _ in range(5):
        actions.send_keys(Keys.ARROW_DOWN)
        actions.perform()
        time.sleep(random.choice(mls_05))




def smoth_scrool(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)


def scroll_to_el(action, el):
    action.pause(time_mls).move_to_element(el).pause(time_mls)


def _in_viewport(driver, element):
    script = (
        "for(var e=arguments[0],f=e.offsetTop,t=e.offsetLeft,o=e.offsetWidth,n=e.offsetHeight;\n"
        "e.offsetParent;)f+=(e=e.offsetParent).offsetTop,t+=e.offsetLeft;\n"
        "return f<window.pageYOffset+window.innerHeight&&t<window.pageXOffset+window.innerWidth&&f+n>\n"
        "window.pageYOffset&&t+o>window.pageXOffset"
    )
    return driver.execute_script(script, element)


def check_dialog_class(driver: webdriver.Chrome, mode):
    try:
        iframe = driver.find_element(By.XPATH, "//div[@id='everystraus_add_blur']")
        if iframe.get_attribute("style") == "display: block;":
            # time.sleep(1)
            but_x = get_x_but(driver)
            if mode == 'PC':
                action = ActionChains(driver)
                # action.scroll_to_element(but_x).pause(time_mls).perform()
                move_to_element(driver, but_x)
                time.sleep(time_mls)
                action.click(but_x).perform()
            elif mode == 'mobile':
                touch_input = PointerInput(POINTER_TOUCH, "touch")
                action = ActionBuilder(driver, mouse=touch_input)

                action.pointer_action.move_to(but_x).pointer_down().move_by(2, 2)
                action.perform()
                time.sleep(time_mls)
                action.pointer_action.move_to(but_x).pointer_down().pointer_up()
                action.perform()
    except:
        # secure.log.write_log('Exception', e)
        pass


def interpolate_move():
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


def move_mouse(action):
    # First, go to your start point or Element:
    # action.move_to_element(start_element)
    # action.perform()

    for mouse_x, mouse_y in zip(interpolate_move()[0], interpolate_move()[1]):
        action.move_by_offset(mouse_x, mouse_y)
        action.perform()
        print(mouse_x, mouse_y)
        secure.log.write_log('move_mouse', f'{mouse_x}, {mouse_y}')


# Функция для выполнения проверки в отдельном потоке
def check_dialog_thread(stop, driver: webdriver.Chrome, mode):
    while True:
        check_dialog_class(driver, mode)
        if stop():
            break
