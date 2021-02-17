import numpy as np
import pandas as pd


def normalise_sheet_data(source):
    if isinstance(source, list) and len(source) > 1:
        columns = [val.lower().strip() for val in source[0]]

        # fill up pandas excel and transform to dictionary(json pattern) data type
        df = pd.DataFrame(source[1:], columns=columns)

        # set index to the column name where is a 'primary key' for your content
        df.set_index('key', inplace=True)
        df = df.replace(np.nan, '', regex=True)
        return df.to_dict()

    else:
        return dict()
