import os

import pandas as pd

from config import countries


def load_datasets(base_path, site_path, sensor_path):
    data = []
    for site in site_path:
        df = pd.read_parquet(str(os.path.join(base_path, site, sensor_path)))
        data.append(df)

    all_df = pd.concat(data)
    all_df.experimentid = all_df.experimentid.replace(countries)
    return all_df
