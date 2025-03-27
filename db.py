import duckdb
import pandas as pd

DB_FILE = "my.db"


def fetch_patients() -> pd.DataFrame:#Получает объединённые данные из представления view1_patients_1 и 
    #возвращает их в виде DataFrame для анализа и визуализации.

    with duckdb.connect(DB_FILE) as duck:
        df = duck.execute("SELECT * FROM view1_patients_1").fetchdf()
        return df
