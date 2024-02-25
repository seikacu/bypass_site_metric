from random import randint

import random
from math import sqrt
from numpy.random import choice
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from utils import get_window_characteristics

STEP = 25


class ActionChainsChild(ActionChains):
    def move_by_offset(self, xoffset, yoffset):
        self.w3c_actions.pointer_action.move_by(xoffset, yoffset)
        return self


def get_location(button):
    size = button.size
    if size['width'] == 0 or size['height'] == 0:
        return -1, -1
    # print(f'size = {size}')
    x = randint(0, size['width'])
    y = randint(0, size['height'])
    return x, y


def get_steps(start_x, start_y, finish_x, finish_y, num_of_steps):
    x_step = (finish_x - start_x) / num_of_steps
    y_step = (finish_y - start_y) / num_of_steps
    return x_step, y_step


def distance(x1, y1, x2, y2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def mouse_move(driver, x, y) -> None:
    ActionChains(driver).move_by_offset(x, y).perform()


def mouse_move_to_element(driver: WebDriver, el: WebElement, mouse) -> bool:
    # Размеры кнопки
    x_bias, y_bias = get_location(el)
    if x_bias == -1.0 and y_bias == -1.0:
        print('x_bias == -1 and y_bias == -1')
        return False
    # Верхняя и нжняя шраница окна по оси Y
    win_upper_bound, _ = get_window_characteristics(driver)
    # print(
    # f"win_upper_bound - {win_upper_bound}; win_lower_bound - {win_lower_bound}")
    x_location = el.location['x']
    y_location = el.location['y'] - win_upper_bound
    # print(f"x_location - {x_location}; y_location - {y_location}")
    num_of_steps = int(distance(mouse.x, mouse.y,
                                x_location, y_location) / STEP)
    # print(f"num_of_steps - {num_of_steps}")
    if num_of_steps:
        x_step, y_step = get_steps(
            mouse.x, mouse.y, x_location, y_location, num_of_steps)
        # print(f"x_step - {x_step}; y_step - {y_step}")
        for _ in range(num_of_steps):
            print(f'x: {mouse.x}, y: {mouse.y}')
            ActionChainsChild(driver).move_by_offset(x_step, y_step).perform()
            mouse.x += x_step
            mouse.y += y_step
    ActionChainsChild(driver).move_to_element_with_offset(
        el, x_bias, y_bias).perform()
    mouse.x += x_bias
    mouse.y += y_bias
    return True


def random_movements(driver, mouse) -> None:
    while True:
        width = driver.execute_script(
            'return document.documentElement.clientWidth')
        height = driver.execute_script(
            'return document.documentElement.clientHeight')
        prob_y = mouse.y / width
        prob_x = mouse.x / height
        move_y = random.uniform(0., 15.) * \
            choice([-1, 1], p=[prob_y, 1 - prob_y])
        move_x = random.uniform(0., 15.) * \
            choice([-1, 1], p=[prob_x, 1 - prob_x])
        mouse.x += move_x
        mouse.y += move_y
        if all(((mouse.x + move_x * 10 < height),
                (mouse.y + move_y * 10 < width),
                (mouse.x + move_x * 10 > 0),
                (mouse.y + move_y * 10 > 0))):
            for _ in range(10):
                print(f'random_movements - x: {mouse.x}, y: {mouse.y}')
                mouse_move(driver, move_x, move_y)
        break


def mouse_click(action):
    action.click().perform()
