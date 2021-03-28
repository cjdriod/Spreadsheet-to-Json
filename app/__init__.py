import os
from json import dump
from app.controllers.auth_controller import AuthController as Auth
from app.controllers.google_service_controller import GoogleServiceController as GService
from config.configuration import (
    SOURCE_1,
    SOURCE_2,
    ACCESS_TOKEN,
    CREDENTIAL_FILE,
    PRESET_OUTPUT_DIRS,
    DEFAULT_OUTPUT_URI,
    ENABLE_EMPTY_DATA_FILTER,
    ARTIFACT_LOOKUP_DICTIONARY
)

selected_output_dir = DEFAULT_OUTPUT_URI or os.path.join(os.getcwd(), 'output')


def serve_application():
    create_logger_dir()

    authentication = Auth(token=ACCESS_TOKEN, default_credential=CREDENTIAL_FILE)
    is_login = authentication.login()

    if is_login:
        job_list = []

        for source in [SOURCE_1, SOURCE_2]:
            if source.get('namespace'):
                job_list.append({
                    "namespace": source.get('namespace'),
                    "sheet_name": source.get('sheet_name'),
                    "sheet_id": source.get('spreadsheet_id'),
                    "primary_key": source.get('primary_key'),
                    "credential": authentication.get_session_credential(),
                    "custom_sheet_range": source.get('custom_sheet_range'),
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
    sheet_id = sheet_meta.get('sheet_id')
    namespace = sheet_meta.get('namespace')
    sheet_name = sheet_meta.get('sheet_name')
    credential = sheet_meta.get('credential')
    primary_key = sheet_meta.get('primary_key')
    custom_range = sheet_meta.get('custom_sheet_range')

    if namespace and sheet_name and sheet_id and credential:
        output_base_uri = os.path.join(selected_output_dir, namespace)

        instance = GService(
            namespace=namespace,
            sheet_id=sheet_id,
            sheet_name=sheet_name,
            credential=credential,
            custom_range=custom_range
        )
        result = instance.retrieve_spreadsheet_content(primary_key)

        if result:
            print()  # for CLI decoration purpose only

            if not os.path.isdir(output_base_uri):
                os.makedirs(output_base_uri)

            artifact_lookup_table = get_output_directory_list(result.get('titles'))
            data_sets = result.get('values')

            for key in artifact_lookup_table:
                export_uri = os.path.join(output_base_uri, '{}.json'.format(artifact_lookup_table.get(key)))

                with open(export_uri, 'w', encoding='utf-8') as json_file:
                    content = data_sets.get(key, dict())

                    if ENABLE_EMPTY_DATA_FILTER:
                        # remove data that hold empty string
                        content = {key: value for (key, value) in content.items() if value}

                    dump(content, json_file, ensure_ascii=False, sort_keys=True, indent=2)
                    json_file.write('\n')

                    print('[{}] Export to {} successfully'.format(namespace, export_uri))


def get_output_directory_list(columns):
    if ARTIFACT_LOOKUP_DICTIONARY:
        return ARTIFACT_LOOKUP_DICTIONARY
    elif isinstance(columns, list) and len(columns):
        return dict(zip(columns, columns))
    return dict()


def create_logger_dir():
    if not os.path.isdir('log'):
        os.makedirs('log')

