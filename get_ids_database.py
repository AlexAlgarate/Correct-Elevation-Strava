import pandas as pd
from sqlalchemy import text
from typing import List


def get_ids_from_database(sql_query: str, engine: str) -> List[int]:
    '''
    Retrieves a list of IDs from a SQL database using the provided query.
    '''
    df: pd.DataFrame = pd.DataFrame(engine.connect().execute(text(sql_query)))
    id_list: List[int] = df['id'].to_list()
    return id_list
