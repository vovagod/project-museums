import datetime
import pandas as pd 
import numpy as np
import json
import logging
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.types import Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.exc import IntegrityError, DataError
from src.engines import sqldb

logger = logging.getLogger(__name__)

LINK = "/home/vova/OpenData/Museums/data-20-structure-4.csv"

TYPE_CONVERSION = {
  "Int32": Integer,
  "string": String,
  "text": Text,
  "object": JSONB,
  "datetime64[ns, Europe/Moscow]": DateTime,
}

# Создаем MetaData объект
#insp = inspect(sqldb.engine)

class CategoryHeader(BaseModel):
    category: str = Field("Категории", description="object")

class LocationHeader(BaseModel):
    location: str = Field("Местоположение", description="string")

class FieldsHeader(BaseModel):
    '''
    Класс описания связывания структуры БД и заголовков csv-файла.
    К примеру, title - имя поля в БД, "Название" - заголовок колонки в csv-файле,
    description="string" - тип, в который данные будут преобразованы в dataframe
    '''

    title: str = Field("Название", description="string")
    address: str = Field("Адрес", description="string")
    entity: str = Field("Юридическое лицо", description="string")
    inn: str = Field("ИНН", description="string")
    affiliation: str = Field("Принадлежность", description="string")
    submission: str = Field("Подчинение", description="string")
    timezone: str = Field("Timezone", description="string")
    teg: str = Field("Тэг", description="object")
    description: str = Field("Описание", description="text")
    website: str = Field("Адрес сайта", description="string")
    email: str = Field("Адрес электронной почты", description="string")
    eipsk: str = Field("Идентификатор ЕИПСК", description="Int32")
    service_name: str = Field("Название сервиса", description="object")
    updated_at: str = Field("Дата последнего обновления записи", description="datetime64[ns, Europe/Moscow]")


class MuseumHeaders(LocationHeader, CategoryHeader, FieldsHeader):

    @classmethod
    def get_json_schema(cls) -> dict[str, dict[str, str]]:
        '''
        Метод преобразования класса в json-схему 
        вида: {'title': {'column': 'Название', 'column_type': 'str'}, ...}
        '''
        elems = cls.model_json_schema()
        return {
            key: {
                "column": val['default'],
                "column_type": val['description']
                } for key, val in elems['properties'].items()
            }

    @classmethod
    def get_titles(cls) -> dict[str, str]:
        '''Возвращающает словарь заголовков csv-файла (key) и имен полей модели (value) '''
        return {val["column"]: key for key, val in cls.get_json_schema().items()}

    
    #@classmethod
    #def get_sql_types(cls, data: list[str]) -> dict[str, str]:
        #'''Метод, возвращающий словарь типов: {'Название': 'string', ...} поправить!!!'''
        #json_schema = cls.get_json_schema()
        #pairs = {key: json_schema[key]["column_type"] for key in data if json_schema.get(key)}
        #return {key: TYPE_CONVERSION[value] for key, value in pairs.items()}
       

    @classmethod
    def get_types(cls):
        '''Метод, возвращающий словарь типов: {'Название': 'string', ...}'''
        return {
            value['column']: value['column_type'] for value in cls.get_json_schema().values()
            }


class DownloadDataFromCsv:
    ''' Класс загрузки данных из csv-файла в БД '''

    REPLACENEMT = '["Общая"]'

    def __init__(self, obj: MuseumHeaders) -> None:
        self.obj = obj
        self.schema = self.obj.get_json_schema()
        self.titles = self.obj.get_titles()
        self.data_types = self.obj.get_types()
        self.df = pd.read_csv(LINK, usecols=self.titles.keys(), on_bad_lines='skip', sep=',') # type: ignore [call-overload]

    def prepare_data(self) -> pd.DataFrame:
        ''' Приведение колонок к заданному типу данных в dataframe '''

        logging.info(f"Prepare_data stage...")
        for label, values in self.df.items():
            logging.info(f"Title: {label}, dtype={values.dtype}, non-null={values.notnull().sum()}")
            values_type = self.data_types.get(label, 'object')
            if values_type == "object":
                self.df[label] = self.df[label].fillna("[]")
                defects = self.df[~self.df[label].str.startswith(("[", "{"), na=False)]
                #print(f"START_WITH: {defects[label]}")
                self.df[label] = np.where(
                    self.df[label].str.startswith(tuple(defects[label])),
                    np.nan,
                    self.df[label]
                    )
            if values_type == "Int32":
                self.df[label] = pd.to_numeric(self.df[label], errors='coerce')
                self.df[label] = self.df[label].fillna(0)
            if values_type == "datetime64[ns, Europe/Moscow]":
                self.df[label] = pd.to_datetime(self.df[label], errors='coerce')
            try:
                #print(f"TYPE: {values_type}")
                self.df[label] = self.df[label].astype(values_type)
            except (ValueError, TypeError, KeyError) as e:
                logging.error(f"Error: {e}")
            self.df.rename(columns={label: self.titles[label]}, inplace=True)
        return self.df

    
    def redefine_column(self, title, target_type):
        ''' Заполнить!!! '''
        try:
            self.df[title] = self.df[title].astype(target_type)
        except ValueError as e:
            logging.error(f"Error: {e}")
        self.df.rename(columns={title: title + "_id"}, inplace=True)
        

    def prepare_unique_records(self, column: str, replacement: str = REPLACENEMT) -> list[dict[str, list[str]]]:
        '''Подготовка уникальных записей для таблицы '''
        
        logging.info(f"Prepare_unique_records stage..., column: {column}")
        column_type = self.schema.get(column)["column_type"]
        #print(f"COLUMN:{column}, TYPE:{column_type}")
        self.df[column] = self.df[column].str.replace("&nbsp", replacement)
        self.df[column] = np.where(
            pd.isnull(self.df[column]),
            replacement,
            self.df[column]
            )
        elem_list = []
        for row in self.df[column].values:
            if column_type == "object":
                elem_list.extend(json.loads(row))
            if column_type == "string":
                elem_list.append(row)
        ready_list = list(set(elem_list))
        ready_list.sort()
        return pd.DataFrame(
            {column: ready_list},
            )

    def prepare_foreignkey_column(self, column: str, pd_data: pd.DataFrame) -> None:

        logging.info(f"Prepare_foreignkey_column stage..., column: {column}")
        renamed = column + "_id"
        for idx in range(len(self.df)):
            row, _ = np.where(pd_data == self.df[column][idx])
            self.df.loc[idx, column] = row[0] + 1
        self.df.rename(columns={column: renamed}, inplace=True)
        self.df[renamed] = self.df[renamed].astype("Int32")
    

    def record_table(self, table: str, data: pd.DataFrame) -> None:
        ''' Метод записи подготовленного dataframe в таблицу БД'''

        logging.info(f"Record_table stage..., table: {table}, table types: {data.dtypes}")

        #if table == "museums":
            #print(f"TEG: {data['teg']}")
        
        #print(f"COLUMN_TITLES: {[*data]}")
        #dtype = self.obj.get_sql_types([*data])
        #print(f"DATA: {data}")

        #columns_table = insp.get_columns(table)
        # Get column information
        #print(f"COLUMN_TABLES: {columns_table}")
        data.index = list(range(1, len(data) + 1))
        try:
            data.to_sql(
                name=table,
                con=sqldb.engine,
                #dtype=dtype,
                if_exists="append", 
                index=True, 
                index_label="id",
                #method="multi",
                chunksize=1000,
                )
        except (IntegrityError, DataError) as e:
            logging.error(f"Error: {e}")


def run_process():

    # инициализация
    init = DownloadDataFromCsv(MuseumHeaders)

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
    record: int = init.record_table("categories", category)
    logging.info(f"В таблицу Category внесено {record} записей")

    # переопределение колонки category в category_id в таблице Category
    init.redefine_column("category", "object")
    logging.info(f"В таблице Category переопределена колонка category в category_id")

    # запись в таблицу Museum
    #data  = pd.DataFrame()
    record: int = init.record_table("museums", data)
    logging.info(f"В таблицу Museum внесено {record} записей")

    # запись в таблицу Location
    #record: int = init.record_table("locations", location)
    #logging.info(f"В таблицу Location внесено {record} записей")


if __name__ == "__main__":
    run_process()
    
