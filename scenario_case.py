import threading
import time
import random

from selenium.webdriver import ActionChains

import math

from numpy.random import choice
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.by import By

from navigation import get_but_main_el_select, apartment_scenario_mob
from navigation import check_dialog_thread
from navigation import get_slideshow_but
from navigation import get_pictures
from navigation import get_slideshow_close
from navigation import apartment_scenario
from navigation import get_but_more
from navigation import get_element_by_href
from navigation import move_to_element
from navigation import random_func_main
from navigation import smoth_scrool

from selen import get_selenium_driver
from selen import get_coordinates
from utils import get_target_locations

time_delay = random.randrange(5, 30)

# url = 'https://www.novostroyki-spb.ru/sk-pik?yclid=10057959807083085825'

'''Используйте touch_actions для имитации операций с пальцами!'''


def start_selen(mode):
    driver = None
    thread = None
    stop_threads = False

    try:
        driver = get_selenium_driver(True, mode)
        # target_latitude, target_longitude = get_coordinates(random.choice(target_locations))
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
        driver.add_cookie({'name': 'everystraus_ref', 'value': f'{random.choice(refers)}'})

        stop_threads = False
        # Создание и запуск потока для выполнения проверки на всплывающее диалоговое окно
        thread = threading.Thread(target=check_dialog_thread, args=(lambda: stop_threads, driver,))
        thread.start()

        if mode == 'PC':
            action = ActionChains(driver)
            links = random_func_main(driver)
            link = str(random.choice(links))
            href = link.split('/')[-1]
            main_el_select = href.split('-')[0]
            but_main_el_select = get_but_main_el_select(driver, main_el_select)
            time.sleep(time_delay)
            driver.save_screenshot("screenshots/screenshot_01.png")
            action.scroll_to_element(but_main_el_select).pause(0.5).perform()
            # smoth_scrool(driver, but_main_el_select)
            time.sleep(time_delay)
            move_to_element(driver, but_main_el_select)
            time.sleep(0.3)
            but_main_el_select.click()
            main_element = get_element_by_href(driver, href)
            time.sleep(time_delay)
            driver.save_screenshot("screenshots/screenshot_02.png")
            # smoth_scrool(driver, main_element)
            action.scroll_to_element(main_element).pause(0.5).perform()
            time.sleep(0.5)
            move_to_element(driver, main_element)
            time.sleep(0.3)
            main_element.click()
            time.sleep(time_delay)
            driver.save_screenshot("screenshots/screenshot_03.png")
            but_more = get_but_more(driver)
            if but_more is None:
                cards_links = driver.find_elements(By.XPATH, "//li[contains(@class,'card-list__item')]")
                hrefs = []
                for card in cards_links:
                    tag_a = card.find_element(By.TAG_NAME, "a")
                    href = tag_a.get_attribute('href')
                    hrefs.append(href)
                if hrefs.__len__() > 0:
                    scenario_building(action, driver, hrefs)
                else:
                    element = get_element_by_href(driver, "/agreement")
                    action.scroll_to_element(element).pause(0.5).perform()
                    # smoth_scrool(driver, element)
                    time.sleep(0.5)
                    driver.save_screenshot("screenshots/screenshot_04.png")
                    move_to_element(driver, element)
                    time.sleep(time_delay)
                    element.click()
                    time.sleep(time_delay)
                    driver.save_screenshot("screenshots/screenshot_05.png")
            else:
                while but_more is not None:
                    time.sleep(time_delay)
                    action.scroll_to_element(but_more).pause(0.5).perform()
                    # smoth_scrool(driver, but_more)
                    time.sleep(0.5)
                    driver.save_screenshot("screenshots/screenshot_06.png")
                    move_to_element(driver, but_more)
                    time.sleep(time_delay)
                    but_more.click()
                    time.sleep(time_delay)
                    driver.save_screenshot("screenshots/screenshot_07.png")
                    but_more = get_but_more(driver)
                cards_links = driver.find_elements(By.XPATH, "//li[contains(@class,'card-list__item')]")
                hrefs = []
                for card in cards_links:
                    tag_a = card.find_element(By.TAG_NAME, "a")
                    href = tag_a.get_attribute('href')
                    hrefs.append(href)
                if hrefs.__len__() > 0:
                    scenario_building(action, driver, hrefs)
        elif mode == 'mobile':
            touch_input = PointerInput(POINTER_TOUCH, "touch")
            action = ActionBuilder(driver, mouse=touch_input)

            links = random_func_main(driver)
            link = str(random.choice(links))
            href = link.split('/')[-1]
            main_el_select = href.split('-')[0]
            but_main_el_select = get_but_main_el_select(driver, main_el_select)
            # добавить рандомные движения мышью
            action.pointer_action.move_to(but_main_el_select).pointer_down().move_by(2, 2)
            action.perform()
            time.sleep(1)
            driver.save_screenshot("screenshots/screenshot_01.png")
            action.pointer_action.move_to(but_main_el_select).pointer_down().pointer_up()
            action.perform()
            time.sleep(time_delay)
            driver.save_screenshot("screenshots/screenshot_02.png")

            main_element = get_element_by_href(driver, href)
            time.sleep(time_delay)
            action.pointer_action.move_to(main_element).pointer_down().move_by(2, 2)
            action.perform()
            time.sleep(1)
            driver.save_screenshot("screenshots/screenshot_03.png")
            action.pointer_action.move_to(main_element).pointer_down().pointer_up()
            action.perform()
            time.sleep(time_delay)
            driver.save_screenshot("screenshots/screenshot_04.png")

            but_more = get_but_more(driver)
            if but_more is None:
                cards_links = driver.find_elements(By.XPATH, "//li[contains(@class,'card-list__item')]")
                hrefs = []
                for card in cards_links:
                    tag_a = card.find_element(By.TAG_NAME, "a")
                    href = tag_a.get_attribute('href')
                    hrefs.append(href)
                if hrefs.__len__() > 0:
                    scenario_building_mob(action, driver, hrefs)
                else:
                    element = get_element_by_href(driver, "/agreement")
                    action.pointer_action.move_to(element).pointer_down().move_by(2, 2)
                    action.perform()
                    time.sleep(1)
                    driver.save_screenshot("screenshots/screenshot_05.png")
                    action.pointer_action.move_to(element).pointer_down().pointer_up()
                    action.perform()
                    time.sleep(time_delay)
                    driver.save_screenshot("screenshots/screenshot_06.png")
            else:
                while but_more is not None:
                    time.sleep(time_delay)
                    action.pointer_action.move_to(but_more).pointer_down().move_by(2, 2)
                    action.perform()
                    time.sleep(1)
                    driver.save_screenshot("screenshots/screenshot_07.png")
                    action.pointer_action.move_to(but_more).pointer_down().pointer_up()
                    action.perform()
                    time.sleep(time_delay)
                    driver.save_screenshot("screenshots/screenshot_08.png")
                    but_more = get_but_more(driver)
                cards_links = driver.find_elements(By.XPATH, "//li[contains(@class,'card-list__item')]")
                hrefs = []
                for card in cards_links:
                    tag_a = card.find_element(By.TAG_NAME, "a")
                    href = tag_a.get_attribute('href')
                    hrefs.append(href)
                if hrefs.__len__() > 0:
                    scenario_building_mob(action, driver, hrefs)

        # driver.get('https://browserleaks.com/canvas')
        # driver.get('https://browserleaks.com/geo')
        # driver.get('https://browserleaks.com/javascript')
        # action = ActionChains(driver)
        # more_button = get_but_more(driver)
        # for _ in range(5):
        #     more_button.send_keys(Keys.ARROW_DOWN)
        #     time.sleep(0.5)  # Adjust sleep duration as needed
        # # action.scroll_to_element(more_button).pause(1).perform()
        # action.click(more_button).pause(1).perform()
        # scroll_to_el(action, more_button)
        # loc_el = get_el_location(more_button)
        # y = loc_el['y']
        # scroll_down_to_element(driver, y)
        # # scroll_down_page(driver)
        # action.move_to_element(more_button)
        # time.sleep(1)
        # # driver.execute_script("arguments[0].scrollIntoView();", more_button[-1])
        # action.perform()

    except Exception as e:
        print(e)
        pass
    finally:
        if driver:
            driver.close()
            driver.quit()
        if thread:
            stop_threads = True
            thread.join()


def properties(element):
    kv = element.text.split(' ', 1)[1].split(', ')
    return {x[0]: x[1] for x in list(map(lambda item: item.split(': '), kv))}


def scenario_building_mob(action, driver, hrefs):
    href = str(random.choice(hrefs))
    href = href.split('/')[-1]
    element = get_element_by_href(driver, href)
    action.pointer_action.move_to(element).pointer_down().move_by(2, 2)
    action.perform()
    time.sleep(1)
    action.pointer_action.move_to(element).pointer_down().pointer_up()
    action.perform()
    time.sleep(time_delay)
    pictures = get_pictures(driver)
    action.pointer_action.move_to(pictures).pointer_down().move_by(2, 2)
    action.perform()
    time.sleep(1)
    action.pointer_action.move_to(pictures).pointer_down().pointer_up()
    action.perform()
    time.sleep(time_delay)
    slide_show = get_slideshow_but(driver)
    action.pointer_action.move_to(slide_show).pointer_down().move_by(2, 2)
    action.perform()
    time.sleep(1)
    action.pointer_action.move_to(slide_show).pointer_down().pointer_up()
    action.perform()
    time.sleep(15)
    slideshow_close = get_slideshow_close(driver)
    action.pointer_action.move_to(slideshow_close).pointer_down().move_by(2, 2)
    action.perform()
    time.sleep(1)
    action.pointer_action.move_to(slideshow_close).pointer_down().pointer_up()
    action.perform()
    time.sleep(time_delay)
    apartment_scenario_mob(action, driver)


def scenario_building(action, driver, hrefs):
    href = str(random.choice(hrefs))
    href = href.split('/')[-1]
    element = get_element_by_href(driver, href)
    action.scroll_to_element(element).pause(0.5).perform()
    # smoth_scrool(driver, element)
    time.sleep(0.5)
    move_to_element(driver, element)
    time.sleep(time_delay)
    element.click()
    time.sleep(time_delay)
    pictures = get_pictures(driver)
    move_to_element(driver, pictures)
    time.sleep(0.5)
    pictures.click()
    time.sleep(time_delay)
    slide_show = get_slideshow_but(driver)
    move_to_element(driver, slide_show)
    time.sleep(0.5)
    slide_show.click()
    time.sleep(15)
    slideshow_close = get_slideshow_close(driver)
    move_to_element(driver, slideshow_close)
    time.sleep(0.5)
    slideshow_close.click()
    time.sleep(time_delay)
    apartment_scenario(driver)


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


def test_use_touch(driver):
    driver.get('https://www.selenium.dev/selenium/web/pointerActionsPage.html')

    pointer_area = driver.find_element(By.ID, "pointerArea")
    touch_input = PointerInput(POINTER_TOUCH, "default touch")
    action = ActionBuilder(driver, mouse=touch_input)
    action.pointer_action.move_to(pointer_area).pointer_down().move_by(2, 2).pointer_up()
    action.perform()

    moves = driver.find_elements(By.CLASS_NAME, "pointermove")
    move_to = properties(moves[0])
    down = properties(driver.find_element(By.CLASS_NAME, "pointerdown"))
    move_by = properties(moves[1])
    up = properties(driver.find_element(By.CLASS_NAME, "pointerup"))

    rect = pointer_area.rect
    center_x = rect["x"] + rect["width"] / 2
    center_y = rect["y"] + rect["height"] / 2

    assert move_to["button"] == "-1"
    assert move_to["pointerType"] == "pen"
    assert move_to["pageX"] == str(math.floor(center_x))
    assert move_to["pageY"] == str(math.floor(center_y))
    assert down["button"] == "0"
    assert down["pointerType"] == "pen"
    assert down["pageX"] == str(math.floor(center_x))
    assert down["pageY"] == str(math.floor(center_y))
    assert move_by["button"] == "-1"
    assert move_by["pointerType"] == "pen"
    assert move_by["pageX"] == str(math.floor(center_x + 2))
    assert move_by["pageY"] == str(math.floor(center_y + 2))
    assert up["button"] == "0"
    assert up["pointerType"] == "pen"
    assert up["pageX"] == str(math.floor(center_x + 2))
    assert up["pageY"] == str(math.floor(center_y + 2))


url = 'https://www.novostroyki-spb.ru/'

links = [
    'https://www.novostroyki-spb.ru/rejting-stroitelnyh-kompanij-sankt-peterburga',
    'https://www.novostroyki-spb.ru/novostroyki-ekonom-klassa',
    'https://www.novostroyki-spb.ru/novosti',
    'https://www.novostroyki-spb.ru/skidki-na-kvartiry',
    'https://www.novostroyki-spb.ru/agreement',
    'https://www.novostroyki-spb.ru/privacy-policy'
]

refers = [
    'https://www.google.com/',
    'https://ya.ru/',
    'https://yandex.ru/',
    'https://mail.ru/',
    'https://nova.rambler.ru/',
    'https://search.yahoo.com/',
    'https://www.bing.com/',
    'https://duckduckgo.com/'
]
