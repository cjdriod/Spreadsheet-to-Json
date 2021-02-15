from datetime import datetime


def main():
    print('\nJob Completed at {}.'.format(datetime.now().strftime("%H:%M:%S")))


if __name__ == '__main__':
    main()