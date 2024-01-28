from typing import Dict
import pandas as pd

def convert_dict_to_df(import_dict: Dict) -> pd.DataFrame:

    # convert to DataFrame
    df = (pd.DataFrame.from_dict(import_dict, 
                                        orient='index', 
                                        columns=['temperature', 'feels_like',
                                                  'rain', 'description', 'city'])
                  .reset_index()
                  .rename(columns={"index": "date"})
                  .assign(date = lambda x: pd.to_datetime(x['date']))
                  )

    return df