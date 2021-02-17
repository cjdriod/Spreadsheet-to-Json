from app import serve_application
from datetime import datetime


def main():
    serve_application()
    print('\nJob Completed at {}.'.format(datetime.now().strftime("%H:%M:%S")))


if __name__ == '__main__':
    main()
