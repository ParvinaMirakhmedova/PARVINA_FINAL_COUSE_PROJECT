import streamlit as st
import pandas as pd
import plotly.express as px
from db import fetch_patients

# Настройки страницы
st.set_page_config(page_title="Diabetes Dashboard", layout="wide")

# Загрузка данных из DuckDB
@st.cache_data #декоратор Streamlit (результат выполнения функции будет кэшироваться (сохраняться в памяти).
#При следующем вызове функции Streamlit не будет запускать её заново, а вернёт уже сохранённые данные 
# — если аргументы функции не изменились.)
def load_data():#вызывает функцию fetch_patients() и возвращает полученные данные — DataFrame.
    return fetch_patients()

df = load_data()

# ---------- ФИЛЬТРЫ ----------
st.sidebar.header("Фильтры")

#  Кнопка сброса фильтров
if st.sidebar.button(" Сбросить фильтры"):
    st.rerun()

# Категориальный фильтр (пол, тип диабета)
def apply_categorical_filter(df, column, label):# Объявляется функция apply_categorical_filter.Она принимает три аргумента:
#df — DataFrame, который нужно фильтровать. #column — имя колонки в этом DataFrame, по которой будет фильтрация. #label — текстовая метка, которая будет показана рядом с фильтром в боковой панели (sidebar) Streamlit.
    if column not in df.columns:  #Проверка: существует ли колонка с таким именем в DataFrame. 
        return df    #Если нет такой колонки, функция просто возвращает исходный DataFrame без изменений — защита от ошибки.
    options = sorted(df[column].unique())#  Получаем уникальные значения в выбранной колонке (например, все уникальные диагнозы или пол) и сортирует их по алфавиту или по порядку значений.
    selected = st.sidebar.multiselect(label, options, default=options) #Создаёт мультиселект в боковой панели Streamlit.
#label — надпись над фильтром (например, "Выберите пол"), options — значения, которые можно выбрать, default=options — по умолчанию все значения выбраны, т.е. фильтр не ограничивает данные.
    return df[df[column].isin(selected)]# Возвращает отфильтрованный датафрейм

if "smoking" in df.columns: # создаем радиофильтр для колонки "Курение"
    options = sorted(df["smoking"].dropna().unique())# Берёт значения из колонки smoking, удаляет пустые значения (NaN) и получает уникальные.
    # Затем сортирует их.
    selected = st.sidebar.radio("Курение", options)
    df = df[df["smoking"] == selected]

# Универсальный числовой фильтр (BMI, возраст, FBG)
def apply_numerical_filter(df, column, label):# Определяется функция apply_numerical_filter. Аргументы:df — DataFrame с данными.
#column — название числовой колонки, по которой будет фильтрация.label — надпись, которая будет отображаться над слайдером в боковой панели.
    if column not in df.columns:# Проверка: если в DataFrame нет такой колонки — просто возвращаем исходные данные без фильтрации
        return df
    min_val, max_val = float(df[column].min()), float(df[column].max())# Получаем минимальное и максимальное значения из указанной числовой колонки.
#Приводим к float, чтобы избежать ошибок, например, при использовании int64.
    selected_range = st.sidebar.slider(label, min_val, max_val, (min_val, max_val))# Создаёт слайдер в боковой панели Streamlit. 
    #Пользователь может выбрать диапазон от min_val до max_val.# По умолчанию слайдер установлен на весь диапазон.
    return df[df[column].between(*selected_range)]
#Фильтрует DataFrame, оставляя строки, где значение в колонке лежит в пределах выбранного диапазона.between(*selected_range) — распаковывает диапазон ((min, max)) и применяет фильтрацию

# Применяем фильтры
df = apply_categorical_filter(df, "sex", "Пол")
df = apply_categorical_filter(df, "dm_type", "Тип диабета")
df = apply_categorical_filter(df, "diabetic_retinopathy", "Диабетическая ретинопатия")
df = apply_numerical_filter(df, "bmi", "BMI")
df = apply_numerical_filter(df, "age", "Возраст")
df = apply_numerical_filter(df, "fbg", "FBG")# ---------- ОСНОВНОЙ КОНТЕНТ ----------
st.title(" Diabetes Patient Dashboard")
st.write(f"Количество записей: {len(df)}")

# Чекбокс: скрывать таблицу
hide_table = st.checkbox(" Скрыть таблицу", value=False)

# Две колонки: таблица слева, визуализация справа
col1, col2 = st.columns([1.2, 2])

with col1:
    if not hide_table:
        st.subheader(" Таблица данных")
        st.dataframe(df)

with col2:
    st.subheader(" Визуализация")

    chart_type = st.selectbox(
        "Выберите тип диаграммы:",
        [
            "Распределение BMI",
            "Распределение FBG",
            "BMI vs FBG (по полу)",
            "Распределение по типу диабета (pie)",
            "Средний возраст по полу (bar)",
            "Тип диабета по возрасту и BMI (scatter)"
        ]
    )
# 1. Гистограмма BMI (индекс массы тела)
    if chart_type == "Распределение BMI" and "bmi" in df.columns:
    # График строится, только если:
    # - выбран тип диаграммы "Распределение BMI"
    # - и колонка "bmi" есть в отфильтрованном датафрейме

        st.plotly_chart(
        px.histogram(     # Построение гистограммы с помощью Plotly Express
            df,           # Источник данных — текущий DataFrame
            x="bmi",      # Значения по оси X — индекс массы тела (BMI)
            nbins=25,     # Количество интервалов (корзин) — 25
            title="Распределение BMI",  # Заголовок графика
            color_discrete_sequence=["#2ca02c"]  # Цвет столбцов — зелёный
        ),
        use_container_width=True  # Растягиваем график на всю ширину контейнера
    )


# 2. Гистограмма FBG (уровень глюкозы натощак)
    elif chart_type == "Распределение FBG" and "fbg" in df.columns:
    # Если выбран график "Распределение FBG" и колонка "fbg" есть в датафрейме

        st.plotly_chart(
        px.histogram(  # Используем Plotly Express для построения гистограммы
            df,        # Источник данных — отфильтрованный DataFrame
            x="fbg",   # Значения по оси X — уровень глюкозы (fasting blood glucose)
            nbins=20,  # Количество интервалов (корзин) — 20
            title="Распределение FBG",  # Заголовок графика
            color_discrete_sequence=["#ff7f0e"]  # Цвет столбцов — ярко-оранжевый
        ),
        use_container_width=True  # График занимает всю ширину контейнера (адаптивно)
    )


# 3. Диаграмма рассеяния: BMI vs FBG, цвет — пол
    elif chart_type == "BMI vs FBG (по полу)" and all(col in df.columns for col in ["bmi", "fbg", "sex"]):
    # График отображается, если:
    # - выбран тип графика "BMI vs FBG (по полу)"
    # - и в датафрейме есть все необходимые колонки: "bmi", "fbg", "sex"

        st.plotly_chart(
        px.scatter(      # Построение диаграммы рассеяния (scatter plot)
            df,          # Источник данных — DataFrame после фильтрации
            x="bmi",     # По оси X — индекс массы тела (BMI)
            y="fbg",     # По оси Y — уровень глюкозы натощак (FBG)
            color="sex", # Цвет точек в зависимости от пола
            title="BMI vs FBG",  # Заголовок графика
            hover_data=["full_name"],  # При наведении отображается имя пациента
            color_discrete_map={       # Задаём цвета вручную:
                "female": "#e377c2",   # розовый для женщин
                "male": "#1f77b4"      # синий для мужчин
            }
        ),
        use_container_width=True  # График растягивается по ширине контейнера
    )


# 4. Круговая диаграмма (pie): распределение по типу диабета
    elif chart_type == "Распределение по типу диабета (pie)" and "dm_type" in df.columns:
    # График отображается, если:
    # - выбран тип графика "Распределение по типу диабета (pie)"
    # - и в датафрейме есть колонка "dm_type" (тип диабета)

        st.plotly_chart(
        px.pie(              # Построение круговой диаграммы (pie chart)
            df,              # Источник данных — DataFrame после фильтрации
            names="dm_type", # Категориальная переменная для сегментов круга
            title="Распределение по типу диабета"  # Заголовок графика
        ),
        use_container_width=True  # График растягивается по ширине контейнера
    )


# 5. Столбчатая диаграмма (bar): средний возраст по полу
    elif chart_type == "Средний возраст по полу (bar)" and all(col in df.columns for col in ["sex", "age"]):
    # График отображается, если:
    # - выбран тип графика "Средний возраст по полу (bar)"
    # - и в датафрейме есть колонки "sex" и "age"

    # Группировка по полу и вычисление среднего возраста
        avg_age = df.groupby("sex")["age"].mean().reset_index()

        st.plotly_chart(
        px.bar(            # Построение столбчатой диаграммы
            avg_age,       # Источник данных — таблица со средними значениями
            x="sex",       # Пол по оси X
            y="age",       # Средний возраст по оси Y
            title="Средний возраст по полу",  # Заголовок графика
            hover_data=["age"],    # Отображение значения при наведении
            text_auto=".1f",       # Подписи на столбцах (1 знак после запятой)
            color="sex",           # Цвета столбцов зависят от пола
            color_discrete_map={   # Задаём конкретные цвета вручную
                "female": "#e377c2",  # розовый
                "male": "#1f77b4"     # синий
            }
        ),use_container_width=True  # Растягиваем график по ширине контейнера
        )
        


# 6. Диаграмма рассеяния (scatter): тип диабета по возрасту и BMI
    elif chart_type == "Тип диабета по возрасту и BMI (scatter)" and all(col in df.columns for col in ["dm_type", "age", "bmi"]):
    # График отображается, если:
    # - выбран тип диаграммы "Тип диабета по возрасту и BMI (scatter)"
    # - и в датафрейме присутствуют все нужные колонки: "dm_type", "age", "bmi"

        st.plotly_chart(
        px.scatter(           # Построение scatter-графика (диаграмма рассеяния)
            df,               # Источник данных — отфильтрованный DataFrame
            x="age",          # Ось X — возраст пациента
            y="bmi",          # Ось Y — индекс массы тела (BMI)
            color="dm_type",  # Цвет точки зависит от типа диабета
            title="Распределение типов диабета по возрасту и BMI",  # Заголовок
            hover_data=["full_name", "sex"]  # При наведении — имя и пол пациента
        ),
        use_container_width=True  # Растягиваем график по ширине контейнера
    )

