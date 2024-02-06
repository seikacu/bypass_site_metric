import random
import threading
import time

from numpy.random import choice
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.by import By

import secure

from navigation import check_dialog_thread
from navigation import get_but_main_el_select
from navigation import get_but_more
from navigation import get_element_by_href
from navigation import get_pictures
from navigation import get_slideshow_but
from navigation import get_slideshow_close
from navigation import move_touch
from navigation import random_func_main
from navigation import scroll_move_click_pc
from navigation import select_by_ref_mob
from navigation import select_by_ref_pc
from selen import get_coordinates
from selen import get_selenium_driver
from utils import get_target_locations

time_delay = random.randrange(5, 30)


def start_selen(mode):
    driver = None
    thread = None
    stop_threads = False

    try:
        driver = get_selenium_driver(True, mode)
        target_locations = get_target_locations()
        target_latitude, target_longitude = get_coordinates(target_locations)
        params = dict({
            "latitude": target_latitude,
            "longitude": target_longitude,
            "accuracy": random.randint(50, 90)
        })
        driver.execute_cdp_cmd("Emulation.setGeolocationOverride", params)
        driver.get(url)
        # driver.add_cookie({'name': 'referer', 'value': f'{random.choice(refers)}'})
        # driver.add_cookie({'name': 'everystraus_ref', 'value': f'{random.choice(refers)}'})

        stop_threads = False
        # Создание и запуск потока для выполнения проверки на всплывающее диалоговое окно
        thread = threading.Thread(target=check_dialog_thread, args=(lambda: stop_threads, driver, mode,))
        thread.start()

        if mode == 'PC':
            action = ActionChains(driver)

            li = select_by_ref_pc(driver)
            teg_a = li.find_element(By.TAG_NAME, 'a')
            hrer_name = teg_a.text
            # href = teg_a.get_attribute("href")
            if hrer_name == 'Все новостройки':
                scroll_move_click_pc(action, driver, li)
                scenario_all_buildings(action, driver)
            elif hrer_name == 'Скидки и Акции':
                scroll_move_click_pc(action, driver, li)
                time.sleep(time_delay)
            elif hrer_name == 'Новости':
                scroll_move_click_pc(action, driver, li)
                time.sleep(time_delay)
                # Добавить рандомный выбор нажатия кнопки, или получить список карточек
                but_more = get_but_more(driver)
                if but_more is None:
                    hrefs = get_cads_links(driver)
                    if hrefs.__len__() > 0:
                        # read_news(action, driver)
                        pass
                else:
                    # while but_more is not None:
                    #     time.sleep(time_delay)
                    #     move_touch(action, driver, but_more)
                    #     time.sleep(time_delay)
                    #     driver.save_screenshot("screenshots/screenshot_08.png")
                    #     but_more = get_but_more(driver)
                    pass
            elif hrer_name == 'Рейтинги':
                scroll_move_click_pc(action, driver, li)
                time.sleep(time_delay)
                # ДОБАВИТЬ РАНДОМНЫЙ ВЫБОР ДЕШЕВЫХ ИЛИ ДОРОГИХ КВАРТИР
                hrefs = get_cads_links(driver)
                if hrefs.__len__() > 0:
                    scenario_building(action, driver, hrefs)
            elif hrer_name == 'Застройщики':
                scroll_move_click_pc(action, driver, li)
                time.sleep(time_delay)
                table = driver.find_elements(By.TAG_NAME, 'tr')
                developer = random.choice(table)
                scroll_move_click_pc(action, driver, developer)
                time.sleep(time_delay)
                hrefs = get_cads_links(driver)
                if hrefs.__len__() > 0:
                    scenario_building(action, driver, hrefs)
        elif mode == 'mobile':
            touch_input = PointerInput(POINTER_TOUCH, "touch")
            action = ActionBuilder(driver, mouse=touch_input)

            li = select_by_ref_mob(action, driver)
            teg_a = li.find_element(By.TAG_NAME, 'a')
            hrer_name = teg_a.text
            # href = teg_a.get_attribute("href")
            if hrer_name == 'Все новостройки':
                move_touch(action, driver, li)
                scenario_all_buildings_mob(action, driver)
            elif hrer_name == 'Скидки и Акции':
                move_touch(action, driver, li)
                time.sleep(time_delay)
            elif hrer_name == 'Рейтинг новостроек':
                move_touch(action, driver, li)
                time.sleep(time_delay)
                # ДОБАВИТЬ РАНДОМНЫЙ ВЫБОР ДЕШЕВЫХ ИЛИ ДОРОГИХ КВАРТИР
                hrefs = get_cads_links(driver)
                if hrefs.__len__() > 0:
                    scenario_building_mob(action, driver, hrefs)
            elif hrer_name == 'Новости рынка':
                move_touch(action, driver, li)
                time.sleep(time_delay)
                # Добавить рандомный выбор нажатия кнопки, или получить список карточек
                hrefs = get_cads_links(driver)
                if hrefs.__len__() > 0:
                    # ДОБАВИТЬ ПРОСМОТР НОВОСТЕЙ
                    pass
            elif hrer_name == 'ТОП-30 застройщиков':
                move_touch(action, driver, li)
                time.sleep(time_delay)
                table = driver.find_elements(By.TAG_NAME, 'tr')
                developer = random.choice(table)
                move_touch(action, driver, developer)
                time.sleep(time_delay)
                hrefs = get_cads_links(driver)
                if hrefs.__len__() > 0:
                    scenario_building_mob(action, driver, hrefs)
            elif hrer_name == 'Все застройщики':
                move_touch(action, driver, li)
                time.sleep(time_delay)
                # ДОРАБОТАТЬ ФУНКЦИОНАЛ
                # Добавить рандомный выбор нажатия кнопки, или получить список карточек
                pass
            elif hrer_name == 'Новостройки Москвы':
                time.sleep(time_delay)
                pass

        # driver.get('https://browserleaks.com/canvas')
        # driver.get('https://browserleaks.com/geo')
        # driver.get('https://browserleaks.com/javascript')

    except WebDriverException as ex:
        secure.log.write_log('WebDriverException', ex)
        pass
    except Exception as e:
        secure.log.write_log('Exception', e)
        print(e)
        pass
    finally:
        if driver:
            driver.close()
            driver.quit()
        if thread:
            stop_threads = True
            thread.join()


def get_cads_links(driver):
    cards_links = driver.find_elements(By.XPATH, "//li[contains(@class,'card-list__item')]")
    hrefs = []
    for card in cards_links:
        tag_a = card.find_element(By.TAG_NAME, "a")
        href = tag_a.get_attribute('href')
        hrefs.append(href)
    return hrefs


def scenario_all_buildings_mob(action, driver):
    links = random_func_main(driver)
    link = str(random.choice(links))
    href = link.split('/')[-1]
    main_el_select = href.split('-')[0]
    but_main_el_select = get_but_main_el_select(driver, main_el_select)
    move_touch(action, driver, but_main_el_select)
    time.sleep(time_delay)
    driver.save_screenshot("screenshots/screenshot_02.png")
    main_element = get_element_by_href(driver, href)
    time.sleep(time_delay)
    move_touch(action, driver, main_element)
    time.sleep(time_delay)
    driver.save_screenshot("screenshots/screenshot_04.png")
    but_more = get_but_more(driver)
    if but_more is None:
        hrefs = get_cads_links(driver)
        if hrefs.__len__() > 0:
            scenario_building_mob(action, driver, hrefs)
        else:
            el = get_element_by_href(driver, "/agreement")
            move_touch(action, driver, el)
            time.sleep(time_delay)
            driver.save_screenshot("screenshots/screenshot_06.png")
    else:
        while but_more is not None:
            time.sleep(time_delay)
            move_touch(action, driver, but_more)
            time.sleep(time_delay)
            driver.save_screenshot("screenshots/screenshot_08.png")
            but_more = get_but_more(driver)
        hrefs = get_cads_links(driver)
        if hrefs.__len__() > 0:
            scenario_building_mob(action, driver, hrefs)


def scenario_all_buildings(action, driver):
    links = random_func_main(driver)
    link = str(random.choice(links))
    href = link.split('/')[-1]
    main_el_select = href.split('-')[0]
    but_main_el_select = get_but_main_el_select(driver, main_el_select)
    time.sleep(time_delay)
    driver.save_screenshot("screenshots/screenshot_01.png")
    scroll_move_click_pc(action, driver, but_main_el_select)
    main_element = get_element_by_href(driver, href)
    time.sleep(time_delay)
    driver.save_screenshot("screenshots/screenshot_02.png")
    scroll_move_click_pc(action, driver, main_element)
    time.sleep(time_delay)
    driver.save_screenshot("screenshots/screenshot_03.png")
    but_more = get_but_more(driver)
    if but_more is None:
        hrefs = get_cads_links(driver)
        if hrefs.__len__() > 0:
            scenario_building(action, driver, hrefs)
        else:
            el = get_element_by_href(driver, "/agreement")
            scroll_move_click_pc(action, driver, el)
            time.sleep(time_delay)
            driver.save_screenshot("screenshots/screenshot_05.png")
    else:
        while but_more is not None:
            time.sleep(time_delay)
            scroll_move_click_pc(action, driver, but_more)
            time.sleep(time_delay)
            driver.save_screenshot("screenshots/screenshot_07.png")
            but_more = get_but_more(driver)
        hrefs = get_cads_links(driver)
        if hrefs.__len__() > 0:
            scenario_building(action, driver, hrefs)


def properties(element):
    kv = element.text.split(' ', 1)[1].split(', ')
    return {x[0]: x[1] for x in list(map(lambda item: item.split(': '), kv))}


def scenario_building_mob(action, driver, hrefs):
    href = str(random.choice(hrefs))
    href = href.split('/')[-1]
    el = get_element_by_href(driver, href)
    move_touch(action, driver, el)
    time.sleep(time_delay)
    pictures = get_pictures(driver)
    move_touch(action, driver, pictures)
    time.sleep(time_delay)
    slide_show = get_slideshow_but(driver)
    move_touch(action, driver, slide_show)
    # !!!!!!!!!!!!!!!!!!!!
    time.sleep(15)
    slideshow_close = get_slideshow_close(driver)
    move_touch(action, driver, slideshow_close)
    time.sleep(time_delay)
    apartment_scenario_mob(action, driver)


def apartment_scenario_mob(action, driver):
    section_house = driver.find_element(By.XPATH, "//section[contains(@class, 'section section-house')]")
    elements = section_house.find_elements(By.XPATH, "//div[contains(@class, 'ui-corner-all ui-state-default')]")
    el = random.choice(elements)
    move_touch(action, driver, el)
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


def scenario_building(action, driver, hrefs):
    href = str(random.choice(hrefs))
    href = href.split('/')[-1]
    el = get_element_by_href(driver, href)
    scroll_move_click_pc(action, driver, el)
    time.sleep(time_delay)
    pictures = get_pictures(driver)
    scroll_move_click_pc(action, driver, pictures)
    time.sleep(time_delay)
    slide_show = get_slideshow_but(driver)
    scroll_move_click_pc(action, driver, slide_show)
    # ПОСЧИТАТЬ КОЛ-ВО КАРТИНОК И НА КАЖДУЮ КАТИНКУ 2 СЕКУНДЫ
    time.sleep(15)
    slideshow_close = get_slideshow_close(driver)
    scroll_move_click_pc(action, driver, slideshow_close)
    time.sleep(time_delay)
    apartment_scenario(action, driver)


def apartment_scenario(action, driver):
    section_house = driver.find_element(By.XPATH, "//section[contains(@class, 'section section-house')]")
    elements = section_house.find_elements(By.XPATH, "//div[contains(@class, 'ui-corner-all ui-state-default')]")
    el = random.choice(elements)
    scroll_move_click_pc(action, driver, el)
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


def random_movements(driver, mouse):
    while True:
        width = driver.execute_script(
            'return document.documentElement.clientWidth')
        height = driver.execute_script(
            'return document.documentElement.clientHeight')
        prob_y = mouse.y / width
        prob_x = mouse.x / height
        move_y = random.uniform(0., 15.) * choice([-1, 1], p=[prob_y, 1 - prob_y])
        move_x = random.uniform(0., 15.) * choice([-1, 1], p=[prob_x, 1 - prob_x])
        mouse.x += move_x
        mouse.y += move_y
        if all(((mouse.x + move_x * 10 < height),
                (mouse.y + move_y * 10 < width),
                (mouse.x + move_x * 10 > 0),
                (mouse.y + move_y * 10 > 0))):
            for _ in range(10):
                mouse_move(driver, move_x, move_y)
            break


def mouse_move(driver, x, y):
    action = ActionChains(driver)
    action.move_by_offset(x, y).perform()


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


url = 'https://www.novostroyki-spb.ru/sk-pik?yclid=10057959807083085823О'
# url = 'https://www.novostroyki-spb.ru/'

links = [
    'https://www.novostroyki-spb.ru/rejting-stroitelnyh-kompanij-sankt-peterburga',
    'https://www.novostroyki-spb.ru/novostroyki-ekonom-klassa',
    'https://www.novostroyki-spb.ru/novosti',
    'https://www.novostroyki-spb.ru/skidki-na-kvartiry',
    'https://www.novostroyki-spb.ru/agreement',
    'https://www.novostroyki-spb.ru/privacy-policy'
]

# refers = [
#     'https://www.google.com/',
#     'https://ya.ru/',
#     'https://yandex.ru/',
#     'https://mail.ru/',
#     'https://nova.rambler.ru/',
#     'https://search.yahoo.com/',
#     'https://www.bing.com/',
#     'https://duckduckgo.com/'
# ]
