import pickle
import logging
import os.path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from config.configuration import SCOPES, LOCALHOST_PORT

logger = logging.getLogger('__name__')
logger.setLevel(logging.ERROR)

file_handler = logging.FileHandler('log/debug.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))

logger.addHandler(file_handler)


class AuthController:
    def __init__(self, token, default_credential):
        self._token = token
        self._default_credential = default_credential
        self.__session_credential = None

    def login(self):
        access_token_file_path = '{}.pickle'.format(self._token)
        credential = None

        if os.path.exists(access_token_file_path):
            with open(access_token_file_path, 'rb') as token:
                credential = pickle.load(token)

        if not (credential and credential.valid):

            try:
                if credential and credential.expired and credential.refresh_token:
                    credential.refresh(Request())

                else:
                    default_credential_dir = '{}.json'.format(self._default_credential)
                    flow = InstalledAppFlow.from_client_secrets_file(default_credential_dir, SCOPES)
                    credential = flow.run_local_server(port=LOCALHOST_PORT)

            except Exception:
                print('Authentication Failed: Unable to reach authentication server')
                logger.error('Unable to get auth token', exc_info=True)
                return 0

            with open(access_token_file_path, 'wb') as token:
                pickle.dump(credential, token)

        self.__session_credential = credential

        return bool(credential)

    def get_session_credential(self):
        return self.__session_credential
