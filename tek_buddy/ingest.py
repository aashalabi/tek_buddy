import numpy as np
import pandas as pd
import minsearch

DATA_PATH = r'..\data\data_cleaned.csv'

def load_index(data_path=DATA_PATH):
    df = pd.read_csv('..\data\data_cleaned.csv')
    df = df.replace({np.nan: 'None'})
    df['id'] = df['id'].astype(str)
    documents = df.to_dict(orient='records')
    index = minsearch.Index(
        text_fields=['id','equipment_type', 'equipment_name', 'maker', 'type_of_maintenance', 'frequency',
        'parts_required'],
        keyword_fields=[id]
    )
    index.fit(documents)
    return index