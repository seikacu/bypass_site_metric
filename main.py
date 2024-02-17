import datetime
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
        time_start = datetime.datetime.now()
        # start_selen(random.choice(mode))
        # start_selen('mobile')
        start_selen('PC')
        time_end = datetime.datetime.now()
        time_diff = time_end - time_start
        tsecs = time_diff.total_seconds()
        print(f'[INFO] Script worked in mode for {tsecs} seconds.')
        secure.log.write_log(
            '[INFO]', f'Script worked in mode {mode} for {tsecs} seconds.')
        time.sleep(time_delay)
    # print('END')


if __name__ == '__main__':
    main()
