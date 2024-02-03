import random

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
    # print('END')


if __name__ == '__main__':
    main()
