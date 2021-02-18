""" Application environment and static variables configuration.

SCOPES identify the permission given to access the google sheet.
refer: https://developers.google.com/sheets/api/guides/authorizing for more details
Must remove token file after modified SCOPES
"""

import os
import json
from decouple import config


def get_concat_data_directory_path(file_name):
    return os.path.join(os.getcwd(), 'data\{}'.format(file_name.strip())) if file_name else None


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

LOCALHOST_PORT = config('LOCALHOST_PORT', cast=int, default=0)

ENABLE_EMPTY_DATA_FILTER = config('EMPTY_DATA_FILTER', cast=bool, default=False)

SOURCE_1 = {
    'namespace': config('SOURCE_1_NAMESPACE', default=None),
    'sheet_name': config('SOURCE_1_SHEET_NAME', default=None),
    'spreadsheet_id': config('SOURCE_1_SPREADSHEET_ID', default=None),
    'credential_path': get_concat_data_directory_path(config('SOURCE_1_CREDENTIAL_FILE_NAME', default=None)),
    'access_token_path': get_concat_data_directory_path(config('SOURCE_1_ACCESS_TOKEN_FILE_NAME', default=None)),
}

SOURCE_2 = {
    'namespace': config('SOURCE_2_NAMESPACE', default=None),
    'sheet_name': config('SOURCE_2_SHEET_NAME', default=None),
    'spreadsheet_id': config('SOURCE_2_SPREADSHEET_ID', default=None),
    'credential_path': get_concat_data_directory_path(config('SOURCE_2_CREDENTIAL_FILE_NAME', default=None)),
    'access_token_path': get_concat_data_directory_path(config('SOURCE_2_ACCESS_TOKEN_FILE_NAME', default=None)),
}

try:
    with open(get_concat_data_directory_path('artifact-export-lookup-table.json')) as f:
        ARTIFACT_LOOKUP_DICTIONARY = json.load(f)

except FileNotFoundError:
    ARTIFACT_LOOKUP_DICTIONARY = {}


try:
    with open(get_concat_data_directory_path('preset-directory.json')) as f:
        PRESET_OUTPUT_DIRS = json.load(f)

except FileNotFoundError:
    PRESET_OUTPUT_DIRS = {}
