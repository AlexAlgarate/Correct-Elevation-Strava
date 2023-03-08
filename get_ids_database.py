import pandas as pd
from sqlalchemy import text, create_engine
from typing import List
# from decouple import config
# from dotenv import load_dotenv

# load_dotenv()


def get_ids_from_database(sql_query: str, engine: str) -> List[int]:
    '''
    Retrieves a list of IDs from a SQL database using the provided query.
    '''
    df: pd.DataFrame = pd.DataFrame(engine.connect().execute(text(sql_query)))
    id_list: List[int] = df['id'].to_list()
    return id_list


# ENGINE = create_engine(config('ENGINE'))
# QUERY = (
#     'SELECT id '
#     'FROM "Summary_Strava" '
#     'WHERE sport_type = \'Run\' and '
#     'total_elevation_gain = \'0\' and '
#     'year > \'2019\';'
# )

# ID_LIST = get_ids_from_database(QUERY, ENGINE)
# print(ID_LIST)
