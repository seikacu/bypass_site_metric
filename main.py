import random
import time

from scenario_case import start_selen


mode = [
    'PC',
    'mobile'
]


def main():
    print('START')
    while True:
        start_selen(random.choice(mode))
        # start_selen('mobile')
        # start_selen('PC')
        time.sleep(60)
    # print('END')


if __name__ == '__main__':
    main()
