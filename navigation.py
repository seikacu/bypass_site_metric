import random
import time

from selenium.webdriver import ActionChains
from selenium.common import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

stop_threads = False
time_delay = random.randrange(3, 10)
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


def apartment_scenario(driver: webdriver.Chrome):
    try:
        section_house = driver.find_element(By.XPATH, "//section[contains(@class, 'section section-house')]")
        elements = section_house.find_elements(By.XPATH, "//div[contains(@class, 'ui-corner-all ui-state-default')]")
        el = random.choice(elements)
        move_to_element(driver, el)
        time.sleep(time_delay)
        el.click()
        # scrol to page down
        # scroll_down_yoffset(driver, el, 50)
        plans = el.find_elements(By.XPATH, "//div[contains(@class, 'grid__cell grid__cell--center-h price-plan-cell')]")
        # images = plans.find_elements(By.TAG_NAME, "//a")
        # img = random.choice(images)
        # time.sleep(time_delay)
        # move_to_element(driver, img)
        # time.sleep(0.5)
        # img.click()
        # time.sleep(time_delay)
        # but_close = driver.find_element(By.XPATH, "//button[contains(@class, 'fancybox__button--close')]")
        # move_to_element(driver, but_close)
        # time.sleep(0.5)
        # but_close.click()
    except NoSuchElementException:
        pass


def apartment_scenario_mob(action, driver: webdriver.Chrome):
    try:
        section_house = driver.find_element(By.XPATH, "//section[contains(@class, 'section section-house')]")
        elements = section_house.find_elements(By.XPATH, "//div[contains(@class, 'ui-corner-all ui-state-default')]")
        el = random.choice(elements)
        action.pointer_action.move_to(el).pointer_down().move_by(2, 2)
        action.perform()
        time.sleep(1)
        action.pointer_action.move_to(el).pointer_down().pointer_up()
        action.perform()
        # scrol to page down
        # scroll_down_yoffset(driver, el, 50)
        plans = el.find_elements(By.XPATH, "//div[contains(@class, 'grid__cell grid__cell--center-h price-plan-cell')]")
        # images = plans.find_elements(By.TAG_NAME, "//a")
        # img = random.choice(images)
        # time.sleep(time_delay)
        # move_to_element(driver, img)
        # time.sleep(0.5)
        # img.click()
        # time.sleep(time_delay)
        # but_close = driver.find_element(By.XPATH, "//button[contains(@class, 'fancybox__button--close')]")
        # move_to_element(driver, but_close)
        # time.sleep(0.5)
        # but_close.click()
    except NoSuchElementException:
        pass


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
        return links_btns[3]
    else:
        return links_btns[4]


func_main = [
    get_hrefs_metro,
    get_hrefs_novostrojki,
    get_hrefs_zhk
]

random_func_main = random.choice(func_main)


# Прокрутить колесо мыши до элемента
def move_to_element(driver: webdriver, element):
    ActionChains(driver).pause(0.5).move_to_element(element).pause(0.5).perform()


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


def smoth_scrool(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)


def scroll_to_el(action, el):
    action.pause(0.5).move_to_element(el).pause(0.5)


def _in_viewport(driver, element):
    script = (
        "for(var e=arguments[0],f=e.offsetTop,t=e.offsetLeft,o=e.offsetWidth,n=e.offsetHeight;\n"
        "e.offsetParent;)f+=(e=e.offsetParent).offsetTop,t+=e.offsetLeft;\n"
        "return f<window.pageYOffset+window.innerHeight&&t<window.pageXOffset+window.innerWidth&&f+n>\n"
        "window.pageYOffset&&t+o>window.pageXOffset"
    )
    return driver.execute_script(script, element)


def check_dialog_class(driver: webdriver.Chrome):
    try:
        iframe = driver.find_element(By.XPATH, "//div[@id='everystraus_add_blur']")
        if iframe.get_attribute("style") == "display: block;":
            time.sleep(1)
            but_x = get_x_but(driver)
            # ДОБАВИТЬ РЕАЛЬНОЕ ПЕРЕМЕЩЕНИЕ МЫШИ ИЛИ ПАЛЬЦА
            but_x.click()
        # action = ActionBuilder(driver)
        # action.pointer_action.move_to_location(8, 8).click()
        # action.perform()
        # action.click()
        # action.perform()
        # el.click()
    except:
        pass


# Функция для выполнения проверки в отдельном потоке
def check_dialog_thread(stop, driver: webdriver.Chrome):
    while True:
        check_dialog_class(driver)
        if stop():
            break
