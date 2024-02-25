import random
import threading
import time
import traceback

from selenium.common.exceptions import (
    ElementNotInteractableException,
    InvalidArgumentException,
    InvalidSelectorException,
    NoSuchDriverException,
    NoSuchElementException,
    UnknownMethodException,
    WebDriverException,
)
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

import secure
from move_mouse import mouse_move_to_element

from navigation import (
    change_developer,
    check_dialog_thread,
    click_by_move,
    get_but_main_el_select,
    get_but_more,
    get_cads_links,
    get_count_img,
    get_element_by_href,
    get_main_but_mob,
    get_min_max_top,
    get_pictures,
    get_pictures_progres,
    get_read_docs,
    get_slideshow_but,
    get_slideshow_close,
    move_touch,
    rand_tap_but_more,
    random_func_main,
    scroll_down_screen,
    scroll_page,
    select_by_ref_mob,
    select_by_ref_pc,
    touch,
)
from selen import get_coordinates, get_selenium_driver
from utils import Mouse, get_target_locations

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


def start_selen(mode: str) -> None:
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
            # Вероятность выбора равна 90%
            if random.random() < 0.9:
                li = select_by_ref_pc(driver)
                teg_a = li.find_element(By.TAG_NAME, 'a')
                hrer_name = teg_a.text
                if hrer_name == 'Все новостройки':
                    scenario_pc_all_new_buildings(driver, li, my_mouse)
                elif hrer_name == 'Скидки и Акции':
                    scenario_pc_discount(driver, li, my_mouse)
                elif hrer_name == 'Новости':
                    scenario_pc_news(driver, li, my_mouse)
                elif hrer_name == 'Рейтинги':
                    scenario_pc_ratings(driver, li, my_mouse)
                elif hrer_name == 'Застройщики':
                    scenario_pc_developers(driver, li, my_mouse)
            else:
                scenario_pc_main(driver, my_mouse)
        elif mode == 'mobile':
            print("mode - mobile")
            secure.log.write_log('mode', 'mobile')
            # Вероятность выбора равна 90%
            if random.random() < 0.9:
                nav_btn = get_main_but_mob(driver)
                touch(driver, nav_btn)
                time.sleep(time_delay)
                li = select_by_ref_mob(driver)
                teg_a = li.find_element(By.TAG_NAME, 'a')
                hrer_name = teg_a.text
                if hrer_name == 'Все новостройки':
                    scenario_mob_all_new_buildings(driver, li)
                elif hrer_name == 'Скидки и Акции':
                    scenario_mob_discount(driver, li)
                elif hrer_name == 'Рейтинг новостроек':
                    scenario_mob_ratings(driver, li)
                elif hrer_name == 'Новости рынка':
                    scenario_mob_news(driver, li)
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
                    time.sleep(time_delay)
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
                    time.sleep(time_delay)
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


def scenario_pc_all_new_buildings(driver: WebDriver, el: WebElement, mouse):
    print("sub mode - Все новостройки")
    secure.log.write_log('sub mode', 'Все новостройки')
    scroll_page(driver, el)
    mouse_move_to_element(driver, el, mouse)
    click_by_move(driver, el)
    time.sleep(time_delay)
    scenario_pc_buildings(driver, mouse)


def scenario_pc_discount(driver: WebDriver, el: WebElement, mouse):
    print("sub mode - Скидки и Акции")
    secure.log.write_log('sub mode', 'Скидки и Акции')
    scroll_page(driver, el)
    mouse_move_to_element(driver, el, mouse)
    click_by_move(driver, el)
    time.sleep(time_delay)
    el = get_read_docs(driver)
    # scroll_page(action, driver, el, my_mouse)
    mouse_move_to_element(driver, el, mouse)
    click_by_move(driver, el)
    time.sleep(time_delay)
    height_end_page = driver.execute_script(
        "return document.body.scrollHeight")
    scroll_down_screen(driver, height_end_page)
    time.sleep(time_delay)


def scenario_pc_news(driver: WebDriver, el: WebElement, mouse):
    print("sub mode - Новости")
    secure.log.write_log('sub mode', 'Новости')
    scroll_page(driver, el)
    mouse_move_to_element(driver, el, mouse)
    click_by_move(driver, el)
    time.sleep(time_delay)
    but_more = get_but_more(driver)
    scrols = random.randrange(1, 10)
    for i in range(0, scrols):
        if but_more is None:
            break
        scroll_page(driver, but_more)
        mouse_move_to_element(driver, but_more, mouse)
        click_by_move(driver, but_more)
        time.sleep(time_delay)
        but_more = get_but_more(driver)
        i += 1
    hrefs = get_cads_links(driver)
    if hrefs.__sizeof__() > 0:
        scenario_pc_read_news(driver, hrefs, mouse)


def scenario_pc_ratings(driver: WebDriver, el: WebElement, mouse):
    print("sub mode - Рейтинги")
    secure.log.write_log('sub mode', 'Рейтинги')
    scroll_page(driver, el)
    mouse_move_to_element(driver, el, mouse)
    click_by_move(driver, el)
    time.sleep(time_delay)
    top = get_min_max_top(driver)
    scroll_page(driver, top)
    mouse_move_to_element(driver, top, mouse)
    click_by_move(driver, top)
    time.sleep(time_delay)
    hrefs = get_cads_links(driver)
    if hrefs.__sizeof__() > 0:
        scenario_pc_building(driver, hrefs, mouse)


def scenario_pc_developers(driver: WebDriver, el: WebElement, mouse):
    print("sub mode - Застройщики")
    secure.log.write_log('sub mode', 'Застройщики')
    scroll_page(driver, el)
    mouse_move_to_element(driver, el, mouse)
    click_by_move(driver, el)
    time.sleep(time_delay)
    table = driver.find_elements(By.TAG_NAME, 'tr')
    random.shuffle(table)
    developer = random.choice(table)
    href = developer.find_element(By.TAG_NAME, 'a')
    scroll_page(driver, href)
    mouse_move_to_element(driver, href, mouse)
    click_by_move(driver, href)
    time.sleep(time_delay)
    hrefs = get_cads_links(driver)
    if hrefs.__sizeof__() > 0:
        scenario_pc_building(driver, hrefs, mouse)


def scenario_pc_main(driver: WebDriver, mouse):
    print("sub mode - main")
    secure.log.write_log('sub mode', 'main')
    time.sleep(time_delay)
    hrefs = get_cads_links(driver)
    if hrefs.__sizeof__() > 0:
        scenario_pc_building(driver, hrefs, mouse)


def scenario_pc_buildings(driver: WebDriver, mouse):
    refs = random_func_main(driver)
    random.shuffle(refs)
    link = str(random.choice(refs))
    href = link.split('/')[-1]
    main_el_select = href.split('-')[0]
    but_main_el_select = get_but_main_el_select(driver, main_el_select)
    # random_movements(driver, mouse)
    scroll_page(driver, but_main_el_select)
    mouse_move_to_element(driver, but_main_el_select, mouse)
    click_by_move(driver, but_main_el_select)
    time.sleep(time_delay)
    main_element = get_element_by_href(driver, href)
    # random_movements(driver, mouse)
    scroll_page(driver, main_element)
    mouse_move_to_element(driver, main_element, mouse)
    click_by_move(driver, but_main_el_select)
    # random_movements(driver, mouse)
    time.sleep(time_delay)
    if main_el_select == 'zhk':
        pictures = get_pictures(driver)
        scenario_pc_apartment(driver, pictures, mouse)
        progres = get_pictures_progres(driver)
        if progres:
            scenario_pc_apartment(driver, progres, mouse)
        else:
            height_end_page = driver.execute_script(
                "return document.body.scrollHeight")
            scroll_down_screen(driver, height_end_page)
            time.sleep(time_delay)
            el = get_read_docs(driver)
            mouse_move_to_element(driver, el, mouse)
            click_by_move(driver, el)
            time.sleep(time_delay)
            height_end_page = driver.execute_script(
                "return document.body.scrollHeight")
            scroll_down_screen(driver, height_end_page)
            time.sleep(time_delay)
    else:
        but_more = get_but_more(driver)
        if but_more is None:
            hrefs = get_cads_links(driver)
            if hrefs.__sizeof__() > 0:
                scenario_pc_building(driver, hrefs, mouse)
            else:
                height_end_page = driver.execute_script(
                    "return document.body.scrollHeight")
                scroll_down_screen(driver, height_end_page)
                time.sleep(time_delay)
                el = get_read_docs(driver)
                mouse_move_to_element(driver, el, mouse)
                click_by_move(driver, el)
                time.sleep(time_delay)
                height_end_page = driver.execute_script(
                    "return document.body.scrollHeight")
                scroll_down_screen(driver, height_end_page)
                time.sleep(time_delay)
        else:
            scrols = random.randrange(1, 10)
            for i in range(0, scrols):
                if but_more is None:
                    break
                scroll_page(driver, but_more)
                mouse_move_to_element(driver, but_more, mouse)
                click_by_move(driver, but_more)
                # random_movements(driver, mouse)
                time.sleep(time_delay)
                but_more = get_but_more(driver)
                i += 1
            hrefs = get_cads_links(driver)
            if hrefs.__sizeof__() > 0:
                scenario_pc_building(driver, hrefs, mouse)


def scenario_pc_building(driver: WebDriver, hrefs: list, mouse):
    random.shuffle(hrefs)
    href = str(random.choice(hrefs))
    href = href.split('/')[-1]
    print(f"href - {href}")
    el = get_element_by_href(driver, href)
    scroll_page(driver, el)
    mouse_move_to_element(driver, el, mouse)
    click_by_move(driver, el)
    # random_movements(driver, mouse)
    time.sleep(time_delay)
    pictures = get_pictures(driver)
    scenario_pc_apartment(driver, pictures, mouse)
    progres = get_pictures_progres(driver)
    if progres:
        scenario_pc_apartment(driver, progres, mouse)
    else:
        height_end_page = driver.execute_script(
            "return document.body.scrollHeight")
        scroll_down_screen(driver, height_end_page)
        time.sleep(time_delay)
        el = get_read_docs(driver)
        mouse_move_to_element(driver, el, mouse)
        click_by_move(driver, el)
        time.sleep(time_delay)
        height_end_page = driver.execute_script(
            "return document.body.scrollHeight")
        scroll_down_screen(driver, height_end_page)
        time.sleep(time_delay)


def scenario_pc_apartment(driver: WebDriver, el: WebElement, mouse):
    scroll_page(driver, el)
    mouse_move_to_element(driver, el, mouse)
    click_by_move(driver, el)
    # random_movements(driver, mouse)
    time.sleep(time_delay)
    count_img = get_count_img(driver)
    # action.send_keys(Keys.SPACE).perform()
    slide_show = get_slideshow_but(driver)
    scroll_page(driver, slide_show)
    mouse_move_to_element(driver, slide_show, mouse)
    click_by_move(driver, slide_show)
    time.sleep(count_img*time_see_pict)
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(time_delay)
    # slideshow_close = get_slideshow_close(driver)
    # scroll_move_click_pc(action, driver, slideshow_close, mouse)
    # mouse_move_to_element(action, driver, mouse, slideshow_close)
    # action.move_to_element(slideshow_close)
    # time.sleep(random.uniform(0.1, 0.5))
    # action.click().perform()
    # random_movements(driver, mouse)

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


def scenario_pc_read_news(driver: WebDriver, hrefs: list, mouse):
    random.shuffle(hrefs)
    href = random.choice(hrefs)
    href = href.split('/')[-1]
    el = get_element_by_href(driver, href)
    scroll_page(driver, el)
    mouse_move_to_element(driver, el, mouse)
    click_by_move(driver, el)
    time.sleep(time_delay)
    height_end_page = driver.execute_script(
        "return document.body.scrollHeight")
    scroll_down_screen(driver, height_end_page)


def scenario_mob_all_new_buildings(driver: WebDriver, el: WebElement):
    print("sub mode - Все новостройки")
    secure.log.write_log('sub mode', 'Все новостройки')
    touch(driver, el)
    time.sleep(time_delay)
    scenario_all_buildings_mob(driver)


def scenario_mob_discount(driver: WebDriver, el: WebElement):
    print("sub mode - Скидки и Акции")
    secure.log.write_log('sub mode', 'Скидки и Акции')
    touch(driver, el)
    time.sleep(time_delay)
    el = get_read_docs(driver)
    move_touch(driver, el)
    time.sleep(time_delay)
    height_end_page = driver.execute_script(
        "return document.body.scrollHeight")
    # Функция листать мобильный экран
    time.sleep(time_delay)


def scenario_mob_ratings(driver: WebDriver, el: WebElement):
    print("sub mode - Рейтинг новостроек")
    secure.log.write_log('sub mode', 'Рейтинг новостроек')
    touch(driver, el)
    time.sleep(time_delay)
    top = get_min_max_top(driver)
    touch(driver, top)
    time.sleep(time_delay)
    hrefs = get_cads_links(driver)
    if hrefs.__sizeof__() > 0:
        scenario_building_mob(driver, hrefs)


def scenario_mob_news(driver: WebDriver, el: WebElement):
    print("sub mode - Новости рынка")
    secure.log.write_log('sub mode', 'Новости рынка')
    touch(driver, el)
    time.sleep(time_delay)
    but_more = get_but_more(driver)
    rand_tap_but_more(driver, but_more)
    time.sleep(time_delay)
    hrefs = get_cads_links(driver)
    if hrefs.__sizeof__() > 0:
        read_news_mob(driver, hrefs)


def scenario_all_buildings_mob(driver):
    refs = random_func_main(driver)
    random.shuffle(refs)
    link = str(random.choice(refs))
    href = link.split('/')[-1]
    main_el_select = href.split('-')[0]
    but_main_el_select = get_but_main_el_select(driver, main_el_select)
    # Как делать скроллинг экрана???
    # move(action)
    touch(driver, but_main_el_select)
    time.sleep(time_delay)
    main_element = get_element_by_href(driver, href)
    move_touch(driver, main_element)
    time.sleep(time_delay)
    if main_el_select == 'zhk':
        pictures = get_pictures(driver)
        apartment_scene_mob(driver, pictures)
        progres = get_pictures_progres(driver)
        if progres:
            apartment_scene_mob(driver, progres)
        else:
            el = get_read_docs(driver)
            move_touch(driver, el)
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
                scenario_building_mob(driver, hrefs)
            else:
                el = get_read_docs(driver)
                move_touch(driver, el)
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
                move_touch(driver, but_more)
                time.sleep(time_delay)
                but_more = get_but_more(driver)
                i += 1
            hrefs = get_cads_links(driver)
            if hrefs.__sizeof__() > 0:
                scenario_building_mob(driver, hrefs)


def scenario_building_mob(driver: WebDriver, hrefs: list):
    random.shuffle(hrefs)
    href = str(random.choice(hrefs))
    href = href.split('/')[-1]
    el = get_element_by_href(driver, href)
    move_touch(driver, el)
    time.sleep(time_delay)
    pictures = get_pictures(driver)
    apartment_scene_mob(driver, pictures)
    progres = get_pictures_progres(driver)
    if progres:
        apartment_scene_mob(driver, progres)
    else:
        el = get_read_docs(driver)
        move_touch(driver, el)
        time.sleep(time_delay)
        # height_end_page = driver.execute_script(
        #     "return document.body.scrollHeight")
        # Функция листать мобильный экран
        # time.sleep(time_delay)


def apartment_scene_mob(driver: WebDriver, el: WebElement):
    move_touch(driver, el)
    time.sleep(time_delay)
    count_img = get_count_img(driver)
    slide_show = get_slideshow_but(driver)
    touch(driver, slide_show)
    time.sleep(count_img*time_see_pict)
    slideshow_close = get_slideshow_close(driver)
    touch(driver, slideshow_close)
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


def read_news_mob(driver: WebDriver, hrefs: list):
    random.shuffle(hrefs)
    href = str(random.choice(hrefs))
    href = href.split('/')[-1]
    el = get_element_by_href(driver, href)
    move_touch(driver, el)
    time.sleep(time_delay)
    # height_end_page = driver.execute_script(
    #     "return document.body.scrollHeight")
    # Функция листать мобильный экран
    el = get_read_docs(driver)
    move_touch(driver, el)
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
