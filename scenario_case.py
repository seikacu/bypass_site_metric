import random
import threading
import time

import secure

from numpy.random import choice
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchDriverException
from selenium.common.exceptions import UnknownMethodException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By

from navigation import check_dialog_thread, scroll_down_screen
from navigation import get_but_main_el_select
from navigation import get_but_more
from navigation import get_cads_links
from navigation import get_element_by_href
from navigation import get_pictures
from navigation import get_pictures_progres
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

time_delay = random.randrange(5, 10)


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
            print("mode - PC")
            secure.log.write_log('mode', 'PC')
            action = ActionChains(driver)

            li = select_by_ref_pc(driver)
            teg_a = li.find_element(By.TAG_NAME, 'a')
            hrer_name = teg_a.text
            if hrer_name == 'Все новостройки':
                print("sub mode - Все новостройки")
                secure.log.write_log('sub mode', 'Все новостройки')
                scroll_move_click_pc(action, driver, li)
                scenario_all_buildings(action, driver)
            elif hrer_name == 'Скидки и Акции':
                print("sub mode - Скидки и Акции")
                secure.log.write_log('sub mode', 'Скидки и Акции')
                scroll_move_click_pc(action, driver, li)
                time.sleep(time_delay)
                el = get_element_by_href(driver, "/agreement")
                scroll_move_click_pc(action, driver, el)
                time.sleep(time_delay)
                el = get_element_by_href(driver, "/agreement")
                scroll_move_click_pc(action, driver, el)
                time.sleep(time_delay)
            elif hrer_name == 'Новости':
                print("sub mode - Новости")
                secure.log.write_log('sub mode', 'Новости')
                scroll_move_click_pc(action, driver, li)
                time.sleep(time_delay)
                but_more = get_but_more(driver)
                # if but_more is None:
                #     hrefs = get_cads_links(driver)
                #     if hrefs.__len__() > 0:
                #         read_news_pc(action, driver, hrefs)
                # else:
                scrols = random.randrange(1, 10)
                for i in range(0, scrols):
                    # time.sleep(time_delay)
                    scroll_move_click_pc(action, driver, but_more)
                    # time.sleep(time_delay)
                    # driver.save_screenshot("screenshots/screenshot_08.png")
                    but_more = get_but_more(driver)
                    i += 1
                hrefs = get_cads_links(driver)
                if hrefs.__len__() > 0:
                    read_news_pc(action, driver, hrefs)
            elif hrer_name == 'Рейтинги':
                print("sub mode - Рейтинги")
                secure.log.write_log('sub mode', 'Рейтинги')
                scroll_move_click_pc(action, driver, li)
                time.sleep(time_delay)
                top = get_min_max_top(driver)
                scroll_move_click_pc(action, driver, top)
                hrefs = get_cads_links(driver)
                if hrefs.__len__() > 0:
                    scenario_building(action, driver, hrefs)
            elif hrer_name == 'Застройщики':
                print("sub mode - Застройщики")
                secure.log.write_log('sub mode', 'Застройщики')
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
            print("mode - mobile")
            secure.log.write_log('mode', 'mobile')
            touch_input = PointerInput(POINTER_TOUCH, "touch")
            action = ActionBuilder(driver, mouse=touch_input)

            li = select_by_ref_mob(action, driver)
            teg_a = li.find_element(By.TAG_NAME, 'a')
            hrer_name = teg_a.text
            if hrer_name == 'Все новостройки':
                print("sub mode - Все новостройки")
                secure.log.write_log('sub mode', 'Все новостройки')
                move_touch(action, driver, li)
                scenario_all_buildings_mob(action, driver)
            elif hrer_name == 'Скидки и Акции':
                print("sub mode - Скидки и Акции")
                secure.log.write_log('sub mode', 'Скидки и Акции')
                move_touch(action, driver, li)
                time.sleep(time_delay)
            elif hrer_name == 'Рейтинг новостроек':
                print("sub mode - Рейтинг новостроек")
                secure.log.write_log('sub mode', 'Рейтинг новостроек')
                move_touch(action, driver, li)
                time.sleep(time_delay)
                top = get_min_max_top(driver)
                move_touch(action, driver, top)
                hrefs = get_cads_links(driver)
                if hrefs.__len__() > 0:
                    scenario_building_mob(action, driver, hrefs)
            elif hrer_name == 'Новости рынка':
                print("sub mode - Новости рынка")
                secure.log.write_log('sub mode', 'Новости рынка')
                move_touch(action, driver, li)
                time.sleep(time_delay)
                but_more = get_but_more(driver)
                if but_more is None:
                    hrefs = get_cads_links(driver)
                    if hrefs.__len__() > 0:
                        read_news_mob(action, driver, hrefs)
                else:
                    rand_tap_more_but(action, but_more, driver)
                    hrefs = get_cads_links(driver)
                    if hrefs.__len__() > 0:
                        read_news_mob(action, driver, hrefs)
            elif hrer_name == 'ТОП-30 застройщиков':
                print("sub mode - ТОП-30 застройщиков")
                secure.log.write_log('sub mode', 'ТОП-30 застройщиков')
                move_touch(action, driver, li)
                time.sleep(time_delay)
                change_developer(action, driver)
                time.sleep(time_delay)
                hrefs = get_cads_links(driver)
                if hrefs.__len__() > 0:
                    scenario_building_mob(action, driver, hrefs)
            elif hrer_name == 'Все застройщики':
                print("sub mode - Все застройщики")
                secure.log.write_log('sub mode', 'Все застройщики')
                move_touch(action, driver, li)
                time.sleep(time_delay)
                but_more = get_but_more(driver)
                rand_tap_more_but(action, but_more, driver)
                change_developer(action, driver)
                time.sleep(time_delay)
                hrefs = get_cads_links(driver)
                if hrefs.__len__() > 0:
                    scenario_building_mob(action, driver, hrefs)
            elif hrer_name == 'Новостройки Москвы':
                print("sub mode - Новостройки Москвы")
                secure.log.write_log('sub mode', 'Новостройки Москвы')
                time.sleep(time_delay)

    except InvalidArgumentException as ex:
        secure.log.write_log('InvalidArgumentException', ex)
        print(ex)
        pass
    except InvalidSelectorException as ex:
        secure.log.write_log('InvalidSelectorException', ex)
        print(ex)
        pass
    except ElementNotInteractableException as ex:
        secure.log.write_log('ElementNotInteractableException', ex)
        print(ex)
        pass
    except UnknownMethodException as ex:
        secure.log.write_log('UnknownMethodException', ex)
        print(ex)
        pass
    except NoSuchDriverException as ex:
        secure.log.write_log('NoSuchDriverException', ex)
        print(ex)
        pass
    except NoSuchElementException as ex:
        secure.log.write_log('NoSuchElementException', ex)
        print(ex)
        pass
    except WebDriverException as ex:
        secure.log.write_log('WebDriverException', ex)
        print(ex)
        pass
    except Exception as e:
        secure.log.write_log('Exception', e)
        print(e)
        pass
    finally:
        if driver:
            # driver.close()
            driver.quit()
        if thread:
            stop_threads = True
            thread.join()


def get_min_max_top(driver):
    punkts = driver.find_elements(By.XPATH, "//div[contains(@class, 'punkt')]")
    punkt = random.choice(punkts)
    parent = punkt.find_element(By.XPATH, "..")
    return parent


def rand_tap_more_but(action, but_more, driver):
    scrols = random.randrange(1, 10)
    for i in range(0, scrols):
        time.sleep(time_delay)
        move_touch(action, driver, but_more)
        time.sleep(time_delay)
        driver.save_screenshot("screenshots/screenshot_08.png")
        but_more = get_but_more(driver)
        i += 1


def change_developer(action, driver):
    table = driver.find_elements(By.TAG_NAME, 'tr')
    developer = random.choice(table)
    move_touch(action, driver, developer)


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
    # driver.save_screenshot("screenshots/screenshot_01.png")
    scroll_move_click_pc(action, driver, but_main_el_select)
    main_element = get_element_by_href(driver, href)
    time.sleep(time_delay)
    # driver.save_screenshot("screenshots/screenshot_02.png")
    scroll_move_click_pc(action, driver, main_element)
    time.sleep(time_delay)
    # driver.save_screenshot("screenshots/screenshot_03.png")
    but_more = get_but_more(driver)
    if but_more is None:
        hrefs = get_cads_links(driver)
        if hrefs.__len__() > 0:
            scenario_building(action, driver, hrefs)
        else:
            el = get_element_by_href(driver, "/agreement")
            scroll_move_click_pc(action, driver, el)
            time.sleep(time_delay)
            el = get_element_by_href(driver, "/agreement")
            scroll_move_click_pc(action, driver, el)
            time.sleep(time_delay)
            # driver.save_screenshot("screenshots/screenshot_05.png")
    else:
        while but_more is not None:
            time.sleep(time_delay)
            scroll_move_click_pc(action, driver, but_more)
            time.sleep(time_delay)
            # driver.save_screenshot("screenshots/screenshot_07.png")
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
    count_img = get_count_img(driver)
    time.sleep(count_img*2)
    slideshow_close = get_slideshow_close(driver)
    move_touch(action, driver, slideshow_close)
    time.sleep(time_delay)
    apartment_scenario_mob(action, driver)


def get_count_img(driver):
    img_count = driver.find_element(By.XPATH, "//span[@data-fancybox-count]")
    return int(img_count.text)


def apartment_scenario_mob(action, driver):
    time.sleep(time_delay)
    section_house = driver.find_element(By.XPATH, "//section[contains(@class, 'section-house')]")
    time.sleep(time_delay)
    elements = section_house.find_elements(By.XPATH, "//div[contains(@class, 'accordion__item-heading')]")
    el = random.choice(elements)
    move_touch(action, driver, el)
    plan = el.find_elements(By.XPATH, "//div[contains(@class, 'price-grid__plan')]")
    time.sleep(time_delay)
    move_touch(action, driver, plan)
    time.sleep(time_delay)
    but_close = driver.find_element(By.XPATH, "//button[contains(@class, 'fancybox__button--close')]")
    move_touch(action, driver, but_close)
    time.sleep(time_delay)


def read_news_pc(action, driver, hrefs):
    href = str(random.choice(hrefs))
    href = href.split('/')[-1]
    el = get_element_by_href(driver, href)
    scroll_move_click_pc(action, driver, el)
    time.sleep(time_delay)
    # ПЕРЕДЕЛАТЬ - ЛИСТАТЬ НОВОСТЬ ДО КОНЦА СТРАНИЦЫ, Т.Е. ЧИТАТЬ
    offset_y = int(driver.get_window_size()['height'])

    scroll_down_screen(action, driver, offset_y)
    # scrols = random.randrange(1, 7)
    # for i in range(0, scrols):
    #     scroll_origin_amount(driver)
    #     time.sleep(time_delay)


def read_news_mob(action, driver, hrefs):
    href = str(random.choice(hrefs))
    href = href.split('/')[-1]
    el = get_element_by_href(driver, href)
    move_touch(action, driver, el)
    time.sleep(time_delay)

    el = get_element_by_href(driver, "/agreement")
    delta_y = random.randint(-90, 90)
    delta_x = random.randint(-90, 90)
    delta_twist = random.randint(0, 90)
    scrols = random.randrange(1, 5)
    # НЕ ЛИСТАЕТ НОВОСТЬ, ПАДАЕТ С ОШИБКОЙ
    for i in range(0, scrols):
        action.pointer_action \
            .move_to(el) \
            .pointer_down() \
            .move_by(2, 2, tilt_x=delta_x, tilt_y=delta_y, twist=delta_twist) \
            .pointer_up(0)
        action.perform()
        time.sleep(time_delay)


def scroll_origin_amount(driver):
    delta_y = random.randint(100, 200)
    origin = driver.find_element(By.TAG_NAME, "h1")
    scroll_origin = ScrollOrigin.from_viewport(origin)
    ActionChains(driver) \
        .scroll_from_origin(scroll_origin, 10, delta_y) \
        .perform()


def scenario_building(action, driver, hrefs):
    href = str(random.choice(hrefs))
    href = href.split('/')[-1]
    el = get_element_by_href(driver, href)
    scroll_move_click_pc(action, driver, el)
    time.sleep(time_delay)
    pictures = get_pictures(driver)
    apartment_scene(action, driver, pictures)

    progres = get_pictures_progres(driver)
    if progres:
        apartment_scene(action, driver, progres)
    else:
        el = get_element_by_href(driver, "/agreement")
        scroll_move_click_pc(action, driver, el)
        time.sleep(time_delay)
        el = get_element_by_href(driver, "/agreement")
        scroll_move_click_pc(action, driver, el)
        time.sleep(time_delay)


def apartment_scene(action, driver, element):
    scroll_move_click_pc(action, driver, element)
    time.sleep(time_delay)
    slide_show = get_slideshow_but(driver)
    scroll_move_click_pc(action, driver, slide_show)
    count_img = get_count_img(driver)
    time.sleep(count_img * 2)
    slideshow_close = get_slideshow_close(driver)
    scroll_move_click_pc(action, driver, slideshow_close)
    time.sleep(time_delay)

    # label = driver.find_element(By.XPATH, "//label[contains(@class, 'filter-checkbox__label apart')]")
    # scroll_move_click_pc(action, driver, label)
    # section_house = driver.find_element(By.XPATH, "//section[contains(@class, 'section-house')]")
    # elements = section_house.find_elements(By.XPATH, "//div[contains(@class, 'accordion__item-heading')]")
    # el = random.choice(elements)
    # scroll_move_click_pc(action, driver, el)
    # # ПУСТОЕ ЗНАЧЕНИЕ - ПРОВЕРИТЬ!!!!
    # plans = el.find_elements(By.XPATH, "//a[contains(@class, 'price-grid__plan')]")
    #
    # scroll_move_click_pc(action, driver, plan)
    # but_close = driver.find_element(By.XPATH, "//button[contains(@class, 'fancybox__button--close')]")
    # scroll_move_click_pc(action, driver, but_close)
    # time.sleep(time_delay)


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
