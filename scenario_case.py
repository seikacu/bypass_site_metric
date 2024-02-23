import random
import threading
import traceback
import time

from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchDriverException
from selenium.common.exceptions import UnknownMethodException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver import Keys
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.by import By

import secure

from move_mouse import mouse_move_to_element
from move_mouse import mouse_click
# from move_mouse import random_movements
from navigation import check_dialog_thread
from navigation import change_developer
from navigation import get_but_main_el_select
from navigation import get_but_more
from navigation import get_cads_links
from navigation import get_element_by_href
from navigation import get_count_img
from navigation import get_main_but_mob
from navigation import get_min_max_top
from navigation import get_pictures
from navigation import get_pictures_progres
from navigation import get_read_docs
from navigation import get_slideshow_but
from navigation import get_slideshow_close
from navigation import move_touch
from navigation import rand_tap_but_more
from navigation import random_func_main
from navigation import scroll_down_screen
from navigation import scroll_move_click_pc
# from navigation import scroll_move_click_pc_2
from navigation import select_by_ref_mob
from navigation import select_by_ref_pc
from navigation import touch
from selen import get_coordinates
from selen import get_selenium_driver
from utils import Mouse
from utils import get_target_locations


# time_delay = random.randrange(5, 10)
# time_see_pict = random.randrange(1, 3)

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


time_delay = random.randrange(3, 7)
time_see_pict = random.randrange(2, 4)


def start_selen(mode: str):
    url = 'https://www.novostroyki-spb.ru/sk-pik?yclid=10057959807083085823О'
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
        my_mouse = Mouse()

        # Создание и запуск потока для выполнения проверки на всплывающее диалоговое окно
        thread = threading.Thread(target=check_dialog_thread, args=(
            lambda: stop_threads, driver, mode, my_mouse,))
        thread.start()

        if mode == 'PC':
            print("mode - PC")
            secure.log.write_log('mode', 'PC')
            action = ActionChains(driver)
            # Вероятность выбора равна 90%
            if random.random() < 0.9:
                li = select_by_ref_pc(driver)
                teg_a = li.find_element(By.TAG_NAME, 'a')
                hrer_name = teg_a.text
                if hrer_name == 'Все новостройки':
                    print("sub mode - Все новостройки")
                    secure.log.write_log('sub mode', 'Все новостройки')
                    # random_movements(driver, my_mouse)
                    # scroll_move_click_pc_2(action, driver, li, my_mouse)
                    scroll_move_click_pc(action, driver, li, my_mouse)
                    mouse_move_to_element(action, driver, my_mouse, li)
                    action.move_to_element(li)
                    time.sleep(random.uniform(0.1, 0.5))
                    action.click().perform()
                    scenario_all_buildings(action, driver, my_mouse)
                elif hrer_name == 'Скидки и Акции':
                    print("sub mode - Скидки и Акции")
                    secure.log.write_log('sub mode', 'Скидки и Акции')
                    scroll_move_click_pc(action, driver, li, my_mouse)
                    mouse_move_to_element(action, driver, my_mouse, li)
                    action.move_to_element(li)
                    time.sleep(random.uniform(0.1, 0.5))
                    action.click().perform()
                    time.sleep(time_delay)
                    # scroll_down_page(driver)
                    # height_end_page = driver.execute_script(
                    #     "return document.body.scrollHeight")
                    # scroll_down_screen(action, driver, height_end_page)
                    # scroll_move_click_pc(action, driver, li, mouse)
                    time.sleep(time_delay)
                    el = get_read_docs(driver)
                    mouse_move_to_element(action, driver, my_mouse, el)
                    action.move_to_element(el)
                    time.sleep(0.5)
                    mouse_click(action)
                    # scroll_move_click_pc_2(action, driver, el, my_mouse)
                    # scroll_move_click_pc(action, driver, el, mouse)
                    time.sleep(time_delay)
                    height_end_page = driver.execute_script(
                        "return document.body.scrollHeight")
                    scroll_down_screen(action, driver, height_end_page)
                    time.sleep(time_delay)
                elif hrer_name == 'Новости':
                    print("sub mode - Новости")
                    secure.log.write_log('sub mode', 'Новости')
                    scroll_move_click_pc(action, driver, li, my_mouse)
                    mouse_move_to_element(action, driver, my_mouse, li)
                    action.move_to_element(li)
                    time.sleep(random.uniform(0.1, 0.5))
                    action.click().perform()
                    # scroll_move_click_pc(action, driver, li, mouse)
                    time.sleep(time_delay)
                    but_more = get_but_more(driver)
                    scrols = random.randrange(1, 10)
                    for i in range(0, scrols):
                        if but_more is None:
                            break
                        # scroll_move_click_pc_2(
                        #     action, driver, but_more, my_mouse)
                        scroll_move_click_pc(
                            action, driver, but_more, my_mouse)
                        mouse_move_to_element(
                            action, driver, my_mouse, but_more)
                        action.move_to_element(but_more)
                        time.sleep(random.uniform(0.1, 0.5))
                        action.click().perform()
                        but_more = get_but_more(driver)
                        time.sleep(time_delay)
                        i += 1
                    hrefs = get_cads_links(driver)
                    if hrefs.__sizeof__() > 0:
                        read_news_pc(action, driver, hrefs, my_mouse)
                elif hrer_name == 'Рейтинги':
                    print("sub mode - Рейтинги")
                    secure.log.write_log('sub mode', 'Рейтинги')
                    scroll_move_click_pc(action, driver, li, my_mouse)
                    mouse_move_to_element(action, driver, my_mouse, li)
                    action.move_to_element(li)
                    time.sleep(random.uniform(0.1, 0.5))
                    action.click().perform()
                    # scroll_move_click_pc(action, driver, li, mouse)
                    time.sleep(time_delay)
                    top = get_min_max_top(driver)
                    scroll_move_click_pc(action, driver, top, my_mouse)
                    mouse_move_to_element(action, driver, my_mouse, top)
                    action.move_to_element(top)
                    time.sleep(random.uniform(0.1, 0.5))
                    action.click().perform()
                    # win_upper_bound, _ = get_window_characteristics(driver)
                    # mouse_move_to_element(driver, top, mouse, win_upper_bound)
                    # move_to_element(driver, top)
                    # time.sleep(time_delay)
                    # action.click(top).perform()
                    hrefs = get_cads_links(driver)
                    if hrefs.__sizeof__() > 0:
                        scenario_building(action, driver, hrefs, my_mouse)
                elif hrer_name == 'Застройщики':
                    print("sub mode - Застройщики")
                    secure.log.write_log('sub mode', 'Застройщики')
                    scroll_move_click_pc(action, driver, li, my_mouse)
                    mouse_move_to_element(action, driver, my_mouse, li)
                    action.move_to_element(li)
                    time.sleep(random.uniform(0.1, 0.5))
                    action.click().perform()
                    # scroll_move_click_pc(action, driver, li, mouse)
                    time.sleep(time_delay)
                    table = driver.find_elements(By.TAG_NAME, 'tr')
                    random.shuffle(table)
                    developer = random.choice(table)
                    href = developer.find_element(By.TAG_NAME, 'a')
                    scroll_move_click_pc(action, driver, href, my_mouse)
                    mouse_move_to_element(action, driver, my_mouse, href)
                    action.move_to_element(href)
                    time.sleep(random.uniform(0.1, 0.5))
                    action.click().perform()
                    # scroll_move_click_pc(action, driver, href, mouse)
                    time.sleep(time_delay)
                    hrefs = get_cads_links(driver)
                    if hrefs.__sizeof__() > 0:
                        scenario_building(action, driver, hrefs, my_mouse)
            else:
                print("sub mode - main")
                secure.log.write_log('sub mode', 'main')
                time.sleep(time_delay)
                hrefs = get_cads_links(driver)
                if hrefs.__sizeof__() > 0:
                    scenario_building(action, driver, hrefs, my_mouse)
        elif mode == 'mobile':
            print("mode - mobile")
            secure.log.write_log('mode', 'mobile')
            touch_input = PointerInput(POINTER_TOUCH, "touch")
            action = ActionBuilder(driver, mouse=touch_input)
            # Вероятность выбора равна 90%
            if random.random() < 0.9:
                nav_btn = get_main_but_mob(driver)
                touch(action, nav_btn)
                time.sleep(time_delay)
                li = select_by_ref_mob(driver)
                teg_a = li.find_element(By.TAG_NAME, 'a')
                hrer_name = teg_a.text
                if hrer_name == 'Все новостройки':
                    print("sub mode - Все новостройки")
                    secure.log.write_log('sub mode', 'Все новостройки')
                    touch(action, li)
                    time.sleep(time_delay)
                    scenario_all_buildings_mob(action, driver)
                elif hrer_name == 'Скидки и Акции':
                    print("sub mode - Скидки и Акции")
                    secure.log.write_log('sub mode', 'Скидки и Акции')
                    touch(action, li)
                    time.sleep(time_delay)
                    el = get_read_docs(driver)
                    move_touch(action, el)
                    height_end_page = driver.execute_script(
                        "return document.body.scrollHeight")
                    # Функция листать мобильный экран
                    time.sleep(time_delay)
                elif hrer_name == 'Рейтинг новостроек':
                    print("sub mode - Рейтинг новостроек")
                    secure.log.write_log('sub mode', 'Рейтинг новостроек')
                    touch(action, li)
                    time.sleep(time_delay)
                    top = get_min_max_top(driver)
                    touch(action, top)
                    hrefs = get_cads_links(driver)
                    if hrefs.__sizeof__() > 0:
                        scenario_building_mob(action, driver, hrefs)
                elif hrer_name == 'Новости рынка':
                    print("sub mode - Новости рынка")
                    secure.log.write_log('sub mode', 'Новости рынка')
                    touch(action, li)
                    time.sleep(time_delay)
                    but_more = get_but_more(driver)
                    rand_tap_but_more(action, but_more, driver)
                    hrefs = get_cads_links(driver)
                    if hrefs.__sizeof__() > 0:
                        read_news_mob(action, driver, hrefs)
                elif hrer_name == 'ТОП-30 застройщиков':
                    print("sub mode - ТОП-30 застройщиков")
                    secure.log.write_log('sub mode', 'ТОП-30 застройщиков')
                    touch(action, li)
                    time.sleep(time_delay)
                    change_developer(action, driver)
                    time.sleep(time_delay)
                    hrefs = get_cads_links(driver)
                    if hrefs.__sizeof__() > 0:
                        scenario_building_mob(action, driver, hrefs)
                elif hrer_name == 'Все застройщики':
                    print("sub mode - Все застройщики")
                    secure.log.write_log('sub mode', 'Все застройщики')
                    touch(action, li)
                    time.sleep(time_delay)
                    but_more = get_but_more(driver)
                    rand_tap_but_more(action, but_more, driver)
                    change_developer(action, driver)
                    time.sleep(time_delay)
                    hrefs = get_cads_links(driver)
                    if hrefs.__sizeof__() > 0:
                        scenario_building_mob(action, driver, hrefs)
                elif hrer_name == 'Новостройки Москвы':
                    print("sub mode - Новостройки Москвы")
                    secure.log.write_log('sub mode', 'Новостройки Москвы')
                    time.sleep(time_delay)
                    touch(action, nav_btn)
                    time.sleep(time_delay)
                    el = get_read_docs(driver)
                    move_touch(action, el)
                    height_end_page = driver.execute_script(
                        "return document.body.scrollHeight")
                    # Функция листать мобильный экран
                    time.sleep(time_delay)
            else:
                print("sub mode - main")
                secure.log.write_log('sub mode', 'main')
                time.sleep(time_delay)
                hrefs = get_cads_links(driver)
                if hrefs.__sizeof__() > 0:
                    scenario_building_mob(action, driver, hrefs)
    except InvalidArgumentException as ex:
        secure.log.write_log('InvalidArgumentException', ex)
        secure.log.write_log('traceback', traceback.format_exc())
        print(ex)
    except InvalidSelectorException as ex:
        secure.log.write_log('InvalidSelectorException', ex)
        secure.log.write_log('traceback', traceback.format_exc())
        print(ex)
    except ElementNotInteractableException as ex:
        secure.log.write_log('ElementNotInteractableException', ex)
        secure.log.write_log('traceback', traceback.format_exc())
        print(ex)
    except UnknownMethodException as ex:
        secure.log.write_log('UnknownMethodException', ex)
        secure.log.write_log('traceback', traceback.format_exc())
        print(ex)
    except NoSuchDriverException as ex:
        secure.log.write_log('NoSuchDriverException', ex)
        secure.log.write_log('traceback', traceback.format_exc())
        print(ex)
    except NoSuchElementException as ex:
        secure.log.write_log('NoSuchElementException', ex)
        secure.log.write_log('traceback', traceback.format_exc())
        print(ex)
    except WebDriverException as ex:
        secure.log.write_log('WebDriverException', ex)
        secure.log.write_log('traceback', traceback.format_exc())
        print(ex)
    except Exception as e:
        secure.log.write_log('Exception', e)
        secure.log.write_log('traceback', traceback.format_exc())
        print(e)
    finally:
        if driver:
            driver.quit()
        if thread:
            stop_threads = True
            thread.join()


def scenario_all_buildings(action, driver, mouse):
    refs = random_func_main(driver)
    random.shuffle(refs)
    link = str(random.choice(refs))
    href = link.split('/')[-1]
    main_el_select = href.split('-')[0]
    but_main_el_select = get_but_main_el_select(driver, main_el_select)
    # random_movements(driver, mouse)
    time.sleep(time_delay)
    scroll_move_click_pc(action, driver, but_main_el_select, mouse)
    mouse_move_to_element(action, driver, mouse, but_main_el_select)
    action.move_to_element(but_main_el_select)
    time.sleep(random.uniform(0.1, 0.5))
    action.click().perform()
    main_element = get_element_by_href(driver, href)
    # random_movements(driver, mouse)
    time.sleep(time_delay)
    scroll_move_click_pc(action, driver, main_element, mouse)
    mouse_move_to_element(action, driver, mouse, main_element)
    action.move_to_element(main_element)
    time.sleep(random.uniform(0.1, 0.5))
    action.click().perform()
    # random_movements(driver, mouse)
    time.sleep(time_delay)
    if main_el_select == 'zhk':
        pictures = get_pictures(driver)
        apartment_scene(action, driver, pictures, mouse)
        progres = get_pictures_progres(driver)
        if progres:
            apartment_scene(action, driver, progres, mouse)
        else:
            height_end_page = driver.execute_script(
                "return document.body.scrollHeight")
            scroll_down_screen(action, driver, height_end_page)
            time.sleep(time_delay)
            el = get_read_docs(driver)
            mouse_move_to_element(action, driver, mouse, el)
            action.move_to_element(el)
            time.sleep(random.choice(mls))
            mouse_click(action)
            # scroll_move_click_pc_2(action, driver, el, mouse)
            time.sleep(time_delay)
            height_end_page = driver.execute_script(
                "return document.body.scrollHeight")
            scroll_down_screen(action, driver, height_end_page)
            time.sleep(time_delay)
    else:
        but_more = get_but_more(driver)
        if but_more is None:
            hrefs = get_cads_links(driver)
            if hrefs.__sizeof__() > 0:
                scenario_building(action, driver, hrefs, mouse)
            else:
                height_end_page = driver.execute_script(
                    "return document.body.scrollHeight")
                scroll_down_screen(action, driver, height_end_page)
                time.sleep(time_delay)
                el = get_read_docs(driver)
                mouse_move_to_element(action, driver, mouse, el)
                action.move_to_element(el)
                time.sleep(0.5)
                mouse_click(action)
                # scroll_move_click_pc_2(action, driver, el, mouse)
                time.sleep(time_delay)
                height_end_page = driver.execute_script(
                    "return document.body.scrollHeight")
                scroll_down_screen(action, driver, height_end_page)
                time.sleep(time_delay)
        else:
            scrols = random.randrange(1, 10)
            for i in range(0, scrols):
                if but_more is None:
                    break
                scroll_move_click_pc(action, driver, but_more, mouse)
                mouse_move_to_element(action, driver, mouse, but_more)
                action.move_to_element(but_more)
                time.sleep(random.uniform(0.1, 0.5))
                action.click().perform()
                # random_movements(driver, mouse)
                time.sleep(time_delay)
                but_more = get_but_more(driver)
                i += 1
            hrefs = get_cads_links(driver)
            if hrefs.__sizeof__() > 0:
                scenario_building(action, driver, hrefs, mouse)


def read_news_pc(action: ActionChains, driver, hrefs: list, mouse):
    random.shuffle(hrefs)
    href = random.choice(hrefs)
    href = href.split('/')[-1]
    el = get_element_by_href(driver, href)
    scroll_move_click_pc(action, driver, el, mouse)
    mouse_move_to_element(action, driver, mouse, el)
    action.move_to_element(el)
    time.sleep(random.uniform(0.1, 0.5))
    action.click().perform()
    # scroll_move_click_pc(action, driver, el, mouse)
    time.sleep(time_delay)
    height_end_page = driver.execute_script(
        "return document.body.scrollHeight")
    scroll_down_screen(action, driver, height_end_page)


def scenario_building(action: ActionChains, driver, hrefs: list, mouse):
    random.shuffle(hrefs)
    href = str(random.choice(hrefs))
    href = href.split('/')[-1]
    print(f"href - {href}")
    el = get_element_by_href(driver, href)
    scroll_move_click_pc(action, driver, el, mouse)
    mouse_move_to_element(action, driver, mouse, el)
    action.move_to_element(el)
    time.sleep(random.uniform(0.1, 0.5))
    action.click().perform()
    # random_movements(driver, mouse)
    time.sleep(time_delay)
    pictures = get_pictures(driver)
    apartment_scene(action, driver, pictures, mouse)
    progres = get_pictures_progres(driver)
    if progres:
        apartment_scene(action, driver, progres, mouse)
    else:
        height_end_page = driver.execute_script(
            "return document.body.scrollHeight")
        scroll_down_screen(action, driver, height_end_page)
        time.sleep(time_delay)
        el = get_read_docs(driver)
        mouse_move_to_element(action, driver, mouse, el)
        action.move_to_element(el)
        time.sleep(random.choice(mls))
        mouse_click(action)
        # scroll_move_click_pc_2(action, driver, el, mouse)
        time.sleep(time_delay)
        height_end_page = driver.execute_script(
            "return document.body.scrollHeight")
        scroll_down_screen(action, driver, height_end_page)
        time.sleep(time_delay)


def apartment_scene(action: ActionChains, driver, el, mouse):
    scroll_move_click_pc(action, driver, el, mouse)
    mouse_move_to_element(action, driver, mouse, el)
    action.move_to_element(el)
    time.sleep(random.uniform(0.1, 0.5))
    action.click().perform()
    # random_movements(driver, mouse)
    time.sleep(time_delay)
    # action.send_keys(Keys.SPACE).perform()
    slide_show = get_slideshow_but(driver)
    scroll_move_click_pc(action, driver, slide_show, mouse)
    mouse_move_to_element(action, driver, mouse, slide_show)
    action.move_to_element(slide_show)
    time.sleep(random.uniform(0.1, 0.5))
    action.click().perform()
    count_img = get_count_img(driver)
    time.sleep(count_img*time_see_pict)
    action.send_keys(Keys.ESCAPE).perform()
    # slideshow_close = get_slideshow_close(driver)
    # scroll_move_click_pc(action, driver, slideshow_close, mouse)
    # mouse_move_to_element(action, driver, mouse, slideshow_close)
    # action.move_to_element(slideshow_close)
    # time.sleep(random.uniform(0.1, 0.5))
    # action.click().perform()
    # random_movements(driver, mouse)
    time.sleep(time_delay)

    # label = driver.find_element(By.XPATH, "//label[contains(@class, 'filter-checkbox__label apart')]")
    # scroll_move_click_pc(action, driver, label)
    # section_house = driver.find_element(By.XPATH, "//section[contains(@class, 'section-house')]")
    # elements = section_house.find_elements(By.XPATH, "//div[contains(@class, 'accordion__item-heading')]")
    # el = random.choice(elements)
    # scroll_move_click_pc(action, driver, el)
    # # ПУСТОЕ ЗНАЧЕНИЕ - ПРОВЕРИТЬ!!!!
    # plans = el.find_elements(By.XPATH, "//a[contains(@class, 'price-grid__plan')]")
    # scroll_move_click_pc(action, driver, plan)
    # but_close = driver.find_element(By.XPATH, "//button[contains(@class, 'fancybox__button--close')]")
    # scroll_move_click_pc(action, driver, but_close)
    # time.sleep(time_delay)


def scenario_all_buildings_mob(action: ActionBuilder, driver):
    refs = random_func_main(driver)
    random.shuffle(refs)
    link = str(random.choice(refs))
    href = link.split('/')[-1]
    main_el_select = href.split('-')[0]
    but_main_el_select = get_but_main_el_select(driver, main_el_select)
    # Как делать скроллинг экрана???
    # move(action)
    touch(action, but_main_el_select)
    time.sleep(time_delay)
    main_element = get_element_by_href(driver, href)
    move_touch(action, main_element)
    time.sleep(time_delay)
    if main_el_select == 'zhk':
        pictures = get_pictures(driver)
        apartment_scene_mob(action, driver, pictures)
        progres = get_pictures_progres(driver)
        if progres:
            apartment_scene_mob(action, driver, progres)
        else:
            el = get_read_docs(driver)
            move_touch(action, el)
            time.sleep(time_delay)
            # height_end_page = driver.execute_script(
            #     "return document.body.scrollHeight")
            # Функция листать мобильный экран
            # time.sleep(time_delay)
    else:
        but_more = get_but_more(driver)
        if but_more is None:
            hrefs = get_cads_links(driver)
            if hrefs.__sizeof__() > 0:
                scenario_building_mob(action, driver, hrefs)
            else:
                el = get_read_docs(driver)
                move_touch(action, el)
                time.sleep(time_delay)
                # height_end_page = driver.execute_script(
                #     "return document.body.scrollHeight")
                # Функция листать мобильный экран
                # time.sleep(time_delay)
        else:
            scrols = random.randrange(1, 10)
            for i in range(0, scrols):
                if but_more is None:
                    break
                time.sleep(time_delay)
                move_touch(action, but_more)
                time.sleep(time_delay)
                but_more = get_but_more(driver)
                i += 1
            hrefs = get_cads_links(driver)
            if hrefs.__sizeof__() > 0:
                scenario_building_mob(action, driver, hrefs)


def scenario_building_mob(action: ActionBuilder, driver, hrefs: list):
    random.shuffle(hrefs)
    href = str(random.choice(hrefs))
    href = href.split('/')[-1]
    el = get_element_by_href(driver, href)
    move_touch(action, el)
    time.sleep(time_delay)
    pictures = get_pictures(driver)
    apartment_scene_mob(action, driver, pictures)
    progres = get_pictures_progres(driver)
    if progres:
        apartment_scene_mob(action, driver, progres)
    else:
        el = get_read_docs(driver)
        move_touch(action, el)
        time.sleep(time_delay)
        # height_end_page = driver.execute_script(
        #     "return document.body.scrollHeight")
        # Функция листать мобильный экран
        # time.sleep(time_delay)


def apartment_scene_mob(action: ActionBuilder, driver, el):
    move_touch(action, el)
    time.sleep(time_delay)
    slide_show = get_slideshow_but(driver)
    touch(action, slide_show)
    count_img = get_count_img(driver)
    time.sleep(count_img*time_see_pict)
    slideshow_close = get_slideshow_close(driver)
    touch(action, slideshow_close)
    time.sleep(time_delay)


# def apartment_scenario_mob(action, driver):
#     time.sleep(time_delay)
#     section_house = driver.find_element(
#         By.XPATH, "//section[contains(@class, 'section-house')]")
#     time.sleep(time_delay)
#     elements = section_house.find_elements(
#         By.XPATH, "//div[contains(@class, 'accordion__item-heading')]")
#     el = random.choice(elements)
#     touch(action, el)
#     plan = el.find_elements(
#         By.XPATH, "//div[contains(@class, 'price-grid__plan')]")
#     time.sleep(time_delay)
#     move_touch(action, driver, plan)
#     time.sleep(time_delay)
#     but_close = driver.find_element(
#         By.XPATH, "//button[contains(@class, 'fancybox__button--close')]")
#     move_touch(action, driver, but_close)
#     time.sleep(time_delay)


def read_news_mob(action: ActionBuilder, driver, hrefs: list):
    random.shuffle(hrefs)
    href = str(random.choice(hrefs))
    href = href.split('/')[-1]
    el = get_element_by_href(driver, href)
    move_touch(action, el)
    time.sleep(time_delay)
    # height_end_page = driver.execute_script(
    #     "return document.body.scrollHeight")
    # Функция листать мобильный экран
    el = get_read_docs(driver)
    move_touch(action, el)
    time.sleep(time_delay)


# url = 'https://www.novostroyki-spb.ru/'

# links = [
#     'https://www.novostroyki-spb.ru/rejting-stroitelnyh-kompanij-sankt-peterburga',
#     'https://www.novostroyki-spb.ru/novostroyki-ekonom-klassa',
#     'https://www.novostroyki-spb.ru/novosti',
#     'https://www.novostroyki-spb.ru/skidki-na-kvartiry',
#     'https://www.novostroyki-spb.ru/agreement',
#     'https://www.novostroyki-spb.ru/privacy-policy'
# ]

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
