import numpy as np
import pandas as pd


def normalise_sheet_data(source, primary_key=None):
    if isinstance(source, list) and len(source) > 1:
        columns = [val.lower().strip() for val in source[0]]
        primary_key_name = (primary_key if primary_key is not None else columns[0]).lower()

        # fill up pandas excel and transform to dictionary(json pattern) data type
        df = pd.DataFrame(source[1:], columns=columns)

        # set index to the column name where is a 'primary key' for your content
        df.set_index(primary_key_name, inplace=True)
        df = df.replace(np.nan, '', regex=True)
        return {
            'titles': [title for title in columns if title != primary_key_name],
            'values': df.to_dict()
        }

    return None
