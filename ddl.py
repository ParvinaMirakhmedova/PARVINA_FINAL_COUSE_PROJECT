import json
import pandas as pd
import duckdb
import os

DB_FILE = 'my.db'

# Удаляем старую БД (если нужна чистая инициализация)
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print("🗑️ Старый файл базы данных удалён.")

# Загружаем описание таблиц
with open('tables.json') as f:
    tables_dict = json.load(f)

# Создание таблиц из SQL
def create_tables():
    try:
        with open('queries/tables.sql') as f:
            tables_query = f.read()

        with duckdb.connect(DB_FILE) as duck:
            duck.execute(tables_query)

            # Отладка: выводим структуру таблиц
            print("\n📋 Структура таблицы patients_1:")
            info = duck.execute("PRAGMA table_info('patients_1')").fetchdf()
            print(info)

        print("\n✅ Tables created successfully")

    except Exception as e:
        print("❌ Ошибка при создании таблиц:", e)

# Чтение листа Excel
def read_xl(sheet_name, columns_dict):
    temp_df = pd.read_excel(
        'source/patients.xlsx',
        sheet_name=sheet_name,
        usecols=columns_dict.keys()
    ).rename(columns=columns_dict)

    # Приведение всех строк к строкам и удаление пробелов
    for col in temp_df.columns:
        if temp_df[col].dtype == object:
            temp_df[col] = temp_df[col].astype(str).str.strip()

    # Упорядочиваем колонки по порядку, указанному в JSON
    expected_order = list(columns_dict.values())
    temp_df = temp_df[expected_order]

    return temp_df

# Вставка данных
def insert_to_db(temp_df, tbl_name):
    with duckdb.connect(DB_FILE) as duck:
        duck.register('temp_table', temp_df)

        # 🟡 Отладка перед вставкой
        print(f"\n🔎 Показ первых строк для {tbl_name}:")
        print(temp_df.head())
        print(temp_df.dtypes)

        # 👇 ЯВНО указываем колонки (чтобы не было путаницы по позициям)
        columns = ", ".join(temp_df.columns)
        duck.execute(f"""
            INSERT INTO {tbl_name} ({columns})
            SELECT {columns} FROM temp_table
        """)

# Создание представлений
def create_views():
    with open('queries/views.sql') as f:
        views = f.read()

    with duckdb.connect(DB_FILE) as duck:
        duck.execute(views)
        duck.commit()

    print("✅ Views were successfully created")

# ETL: Excel → DuckDB
def xl_etl(sheet_name, columns_dict, tbl_name):
    print(f"📥 Inserting data to {tbl_name}...")
    temp_df = read_xl(sheet_name, columns_dict)
    insert_to_db(temp_df, tbl_name)

# Главный pipeline
def create_n_insert():
    print("🚀 Запуск create_n_insert")

    create_tables()

    for k, v in tables_dict.items():
        xl_etl(k, v["columns"], v["table_name"])

    print("✅ Data inserted successfully")

    create_views()

# Запуск
if __name__ == "__main__":
    create_n_insert()
