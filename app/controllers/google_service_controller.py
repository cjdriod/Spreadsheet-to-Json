import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.models.dictionary_creation_model import normalise_sheet_data

logger = logging.getLogger('__name__')
logger.setLevel(logging.ERROR)

file_handler = logging.FileHandler('log/debug.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))

logger.addHandler(file_handler)


class GoogleServiceController:
    __sheet_instance = None

    def __init__(self, namespace, sheet_id, sheet_name, credential, custom_range=None):
        self._namespace = namespace
        self._sheet_id = sheet_id
        self._sheet_range = '\'{}\'{}'.format(sheet_name, custom_range and '!{}'.format(custom_range) or '')

        try:
            service = build(serviceName='sheets', version='v4', credentials=credential)
            self.__sheet_instance = service.spreadsheets()

        except Exception:
            logger.error('Failed to initialize spreadsheet service', exc_info=True)
            print('Failed to establish connection with Google services, please check your internet connection')

    def retrieve_spreadsheet_content(self, primary_key=None):
        if self.__sheet_instance:
            try:
                payload = self.__sheet_instance.values().get(spreadsheetId=self._sheet_id, range=self._sheet_range)
                response = payload.execute()

                self.__sheet_instance.close()
                return normalise_sheet_data(response.get('values', []), primary_key=primary_key)

            except HttpError:
                logger.error('No sheet data found', exc_info=True)
                print('No data found for spreadsheet ID = [{}], sheet name = [{}]'
                      '\nPlease ensure both sheet ID and name is correct'
                      .format(self._sheet_id, self._sheet_range))

            except KeyError:
                logger.error('Invalid JSON object key references', exc_info=True)
                print('Invalid primary key = {}'.format(primary_key))

        return 0
