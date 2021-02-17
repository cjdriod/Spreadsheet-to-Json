from googleapiclient.discovery import build
from app.models.dictionary_creation_model import normalise_sheet_data


class GoogleServiceController:
    __sheet_instance = None

    def __init__(self, namespace, sheet_id, sheet_name, credential):
        self._namespace = namespace
        self._sheet_id = sheet_id
        self._sheet_name = sheet_name

        try:
            service = build(serviceName='sheets', version='v4', credentials=credential)
            self.__sheet_instance = service.spreadsheets()
        except Exception as error:
            # TODO: log error to file
            print('Failed to establish connection with Google services, please check your internet connection')

    def retrieve_spreadsheet_content(self):
        if self.__sheet_instance:
            result = None

            try:
                payload = self.__sheet_instance.values().get(spreadsheetId=self._sheet_id, range=self._sheet_name)
                response = payload.execute()

                self.__sheet_instance.close()
                return normalise_sheet_data(response.get('values', []))

            except Exception as error:
                # TODO: log error to file
                print((result and 'Failed to output file for namespace = {}'.format(self._namespace)) or error)

                return None
