import argparse
import json
import logging

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
from sqlalchemy.exc import DataError, DBAPIError, IntegrityError

from museums.config import BASE_DIR  # type:ignore  [import-untyped]
from museums.engines import sqldb  # type:ignore  [import-untyped]
from museums.models.museum_tables import (  # type:ignore  [import-untyped]
    Category,
    Location,
    Museum,
)
from museums.utils.clean_tables import CleanTables  # type:ignore  [import-untyped]

logger = logging.getLogger(__name__)

LINK = BASE_DIR + "/data/data-20-structure-4.csv"


class ModelFileBinder(BaseModel):
    """
    Класс связывающий структуру БД и csv-файл.
    Атрибуты класса являются именами полей в модели БД. Первый аргумент
    конструктора Field ("Название") - заголовок колонки в csv-файле,
    второй (description="string") - тип, в который данные будут преобразованы
    в dataframe.
    """

    title: str = Field("Название", description="string")
    address: str = Field("Адрес", description="string")
    category: str = Field("Категории", description="object")
    location: str = Field("Местоположение", description="string")
    entity: str = Field("Юридическое лицо", description="string")
    inn: str = Field("ИНН", description="string")
    affiliation: str = Field("Принадлежность", description="string")
    submission: str = Field("Подчинение", description="string")
    timezone: str = Field("Timezone", description="string")
    teg: str = Field("Тэг", description="object")
    description: str = Field("Описание", description="string")
    website: str = Field("Адрес сайта", description="string")
    email: str = Field("Адрес электронной почты", description="string")
    eipsk: str = Field("Идентификатор ЕИПСК", description="Int32")
    service_name: str = Field("Название сервиса", description="object")
    updated_at: str = Field("Дата последнего обновления записи", description="datetime64[ns, Europe/Moscow]")


class SchemaConverter(ModelFileBinder):
    """Класс преобразования схемы ModelFileBinder в структуры Python"""

    @classmethod
    def get_json_schema(cls) -> dict[str, dict[str, str]]:
        """
        Метод преобразования схемы класса в json-схему
        вида: {'title': {'column': 'Название', 'column_type': 'str'}, ...}
        """
        elems: dict = cls.model_json_schema()
        return {
            key: {"column": val["default"], "column_type": val["description"]}
            for key, val in elems["properties"].items()
        }

    @classmethod
    def get_titles(cls) -> dict[str, str]:
        """Метод возвращает словарь заголовков csv-файла (key) и имен полей модели (value)"""
        return {val["column"]: key for key, val in cls.get_json_schema().items()}

    @classmethod
    def get_types(cls) -> dict[str, str]:
        """Метод возвращает словарь типов: {'Название': 'string', ...}"""
        return {value["column"]: value["column_type"] for value in cls.get_json_schema().values()}


class DownloadDataFromCsv:
    """Класс загрузки данных из csv-файла в БД"""

    REPLACEMENT = '["Общая"]'

    def __init__(self, converter: "SchemaConverter", link: str = LINK) -> None:
        self.converter = converter
        self.schema = self.converter.get_json_schema()
        self.titles = self.converter.get_titles()
        self.data_types = self.converter.get_types()
        self.link = link
        self.df = self.read_file()  # type:ignore [no-untyped-call]

    def read_file(self):  # type:ignore [no-untyped-def]
        """Чтение csv-файла"""
        logging.info(f"Reading file {self.link} ...")
        try:
            return pd.read_csv(
                self.link,
                usecols=self.titles.keys(),
                on_bad_lines="skip",
                sep=",",
                low_memory=False,
            )
        except (DataError, TypeError, OSError) as e:
            logging.error(f"Error: {e}")
            raise ValueError

    def prepare_data(self) -> pd.DataFrame:
        """Приведение колонок csv-файла к заданному типу данных в dataframe"""

        logging.info("Prepare_data stage...")
        for label, values in self.df.items():
            logging.info(f"Title: {label}, dtype={values.dtype}, non-null={values.notnull().sum()}")
            values_type = self.data_types.get(label, "object")
            if values_type == "object":
                self.df[label] = self.df[label].fillna("[]")
                defects = self.df[~self.df[label].str.startswith(("[", "{"), na=False)]
                self.df[label] = np.where(self.df[label].str.startswith(tuple(defects[label])), np.nan, self.df[label])
            if values_type == "Int32":
                self.df[label] = pd.to_numeric(self.df[label], errors="coerce")
                self.df[label] = self.df[label].fillna(0)
            if values_type == "datetime64[ns, Europe/Moscow]":
                self.df[label] = pd.to_datetime(self.df[label], errors="coerce")
            try:
                self.df[label] = self.df[label].astype(values_type)
            except (ValueError, TypeError, KeyError) as e:
                logging.error(f"Error: {e}")
            self.df.rename(columns={label: self.titles[label]}, inplace=True)
        return self.df  # type:ignore [no-any-return]

    def redefine_column(self, title: str, target_type: str) -> None:
        """Переопределение колонок в dataframe добавлением постфикса _id"""
        try:
            self.df[title] = self.df[title].astype(target_type)
        except ValueError as e:
            logging.error(f"Error: {e}")
        self.df.rename(columns={title: title + "_id"}, inplace=True)

    def prepare_unique_records(self, column: str, replacement: str = REPLACEMENT) -> pd.DataFrame:
        """Получение списка уникальных записей из заданной колонки"""

        logging.info(f"Prepare_unique_records stage..., column: {column}")
        column_type = self.schema.get(column)["column_type"]  # type:ignore [index]
        self.df[column] = self.df[column].str.replace("&nbsp", replacement)
        self.df[column] = np.where(pd.isnull(self.df[column]), replacement, self.df[column])
        elem_list = []
        for row in self.df[column].values:
            if column_type == "object":
                elem_list.extend(json.loads(row))
            if column_type == "string":
                elem_list.append(row)
        ready_list = list(set(elem_list))
        ready_list.sort()
        return pd.DataFrame({column: ready_list})

    def prepare_foreignkey_column(self, column: str, pd_data: pd.DataFrame) -> None:
        """Преобразование колонки dataframe в колонку внешней связи с другой таблицей"""

        logging.info(f"Prepare_foreignkey_column stage..., column: {column}")
        renamed = column + "_id"
        for idx in range(len(self.df)):
            row, _ = np.where(pd_data == self.df[column][idx])
            self.df.loc[idx, column] = row[0] + 1
        self.df.rename(columns={column: renamed}, inplace=True)
        self.df[renamed] = self.df[renamed].astype("Int32")

    def record_table(self, table: str, data: pd.DataFrame, engine=sqldb.engine) -> int:  # type:ignore [no-untyped-def]
        """Запись подготовленного dataframe в таблицу БД"""

        logging.info(f"Record_table stage..., table: {table}, table types: {data.dtypes}")
        data.index = list(range(1, len(data) + 1))
        try:
            data.to_sql(
                name=table,
                con=engine,
                if_exists="append",
                index=True,
                index_label="id",
                method="multi",
                chunksize=1000,
            )
        except (DBAPIError, IntegrityError, DataError) as e:
            logging.error(f"Error: {e.args[0]}")
            return 0
        return len(data)


def run_process(*args: str) -> None:
    """Целевой процесс записи csv-файла в БД"""

    if "clean" in args:
        CleanTables([Location, Category, Museum]).clean()
        return

    # инициализация
    try:
        init = DownloadDataFromCsv(SchemaConverter)  # type:ignore [arg-type]
    except ValueError:
        return

    # подготовка датафрейма
    data: pd.DataFrame = init.prepare_data()

    # подготовка записей для таблицы Location
    location: pd.DataFrame = init.prepare_unique_records("location")

    # перезапись колонки location в Museum как foreignkey к таблице Location
    init.prepare_foreignkey_column("location", location)

    # запись в таблицу Location
    record = init.record_table("locations", location)
    logging.info(f"В таблицу Locations внесено {record} записей")

    # подготовка записей для таблицы Category
    category: pd.DataFrame = init.prepare_unique_records("category")

    # запись в таблицу Category
    record = init.record_table("categories", category)
    logging.info(f"В таблицу Category внесено {record} записей")

    # переопределение колонки category в category_id в таблице Category
    init.redefine_column("category", "object")
    logging.info("В таблице Category переопределена колонка category в category_id")

    # запись в таблицу Museum
    record = init.record_table("museums", data)
    logging.info(f"В таблицу Museum внесено {record} записей")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-run", help="выполнить очистку таблицы: -run clean")
    args = parser.parse_args()
    run_process(args.run)
