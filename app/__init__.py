import os
from json import dump
from app.controllers.auth_controller import AuthController as Auth
from app.controllers.google_service_controller import GoogleServiceController as GService
from config.configuration import (
    SOURCE_1,
    SOURCE_2,
    ARTIFACT_LOOKUP_DICTIONARY,
    PRESET_OUTPUT_DIRS,
    ENABLE_EMPTY_DATA_FILTER
)

selected_output_dir = os.path.join(os.getcwd(), 'output')


def serve_application():
    job_list = []

    for source in [SOURCE_1, SOURCE_2]:
        if source.get('namespace'):
            instance = Auth(token=source.get('access_token_path'), default_credential=source.get('credential_path'))
            result = instance.login()

            if result:
                job_list.append({
                    "namespace": source.get('namespace'),
                    "sheet_name": source.get('sheet_name'),
                    "sheet_id": source.get('spreadsheet_id'),
                    "credential": instance.get_session_credential(),
                })

    render_preset_directory_selection_options()

    print('Selected output directory: {}'.format(selected_output_dir))

    print('Working on, please wait...')

    for job in job_list:
        generate_json_file(job)


def render_preset_directory_selection_options():
    preset_directories = PRESET_OUTPUT_DIRS.get('directories', [])

    if len(preset_directories):
        for directory in preset_directories:
            if directory.get('index'):
                print('{}: {}'.format(directory.get('index'), directory.get('name')), end='  ')

        user_selection = input('\nSelection (default): => ')
        # Only return the 1st meet result
        result = next((dir_meta for dir_meta in preset_directories
                       if user_selection and (dir_meta.get('index') == user_selection)), None)

        if result:
            global selected_output_dir
            selected_output_dir = result.get('path', selected_output_dir)

    os.system((os.name == 'nt' and 'cls') or 'clear')


def generate_json_file(sheet_meta):
    namespace = sheet_meta.get('namespace')
    sheet_name = sheet_meta.get('sheet_name')
    sheet_id = sheet_meta.get('sheet_id')
    credential = sheet_meta.get('credential')

    if namespace and sheet_name and sheet_id and credential:
        output_base_uri = os.path.join(selected_output_dir, namespace)

        instance = GService(namespace=namespace, sheet_id=sheet_id, sheet_name=sheet_name, credential=credential)
        result = instance.retrieve_spreadsheet_content()

        if result:
            print()  # for CLI decoration purpose only

            if not os.path.isdir(output_base_uri):
                os.makedirs(output_base_uri)

            for key in ARTIFACT_LOOKUP_DICTIONARY:
                export_uri = os.path.join(output_base_uri, ARTIFACT_LOOKUP_DICTIONARY.get(key))

                with open(export_uri, 'w', encoding='utf-8') as json_file:
                    data = result.get(key, dict())

                    if ENABLE_EMPTY_DATA_FILTER:
                        # remove data that hold empty string
                        data = {key: value for (key, value) in data.items() if value}

                    dump(data, json_file, ensure_ascii=False, sort_keys=True, indent=2)
                    json_file.write('\n')

                    print('Export to {} successfully [{}]'.format(export_uri, namespace))
