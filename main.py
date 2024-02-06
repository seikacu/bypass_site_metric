import random
import time

import secure

from scenario_case import start_selen


mode = [
    'PC',
    'mobile'
]

time_delay = random.randrange(10, 60)


def main():
    print('START')
    secure.log.create_log()
    while True:
        start_selen(random.choice(mode))
        # start_selen('mobile')
        # start_selen('PC')
        time.sleep(time_delay)
    # print('END')


if __name__ == '__main__':
    main()
