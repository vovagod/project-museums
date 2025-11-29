import pandas as pd 
import numpy as np
import json
from pydantic import BaseModel, Field
from typing import List, Dict
from enum import Enum
from sqlalchemy.ext.asyncio import create_async_engine
from db import database


#DATABASE_URL = settings.get_db_url()
#engine = create_async_engine(DATABASE_URL, echo=False)

LINK = "/home/vova/OpenData/Museums/data-20-structure-4.csv"

class CategoryHeader(BaseModel):
    category: str = Field("items", description="dict")

class LocationHeader(BaseModel):
    location: str = Field("Местоположение", description="str")

class FieldsHeader(BaseModel):
    '''
    Класс описания связывания структуры БД и заголовков csv-файла.
    Здесь, к примеру, title - имя поля в БД, "Название" - заголовок колонки в csv-файле,
    description="str" - тип, в котором находятся данные в этой колонке
    '''

    title: str = Field("Название", description="str")
    address: str = Field("Адрес", description="str")
    entity: str = Field("Юридическое лицо", description="str")
    inn: int = Field("ИНН", description="int")
    affiliation: str = Field("Принадлежность", description="str")
    submission: str = Field("Подчинение", description="str")
    timezone: str = Field("Timezone", description="str")
    teg: str = Field("Тэг", description="dict")
    description: str = Field("Описание", description="str")
    website: str = Field("Адрес сайта", description="str")
    email: str = Field("Адрес электронной почты", description="str")
    eipsk: int = Field("Идентификатор ЕИПСК", description="int")


class MuseumHeaders(LocationHeader, CategoryHeader, FieldsHeader):

    @classmethod
    def get_json_schema(cls):
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
    def get_columns(cls):
        '''Метод, возвращающий список заголовков csv-файла'''
        return [val["column"] for key, val in cls.get_json_schema().items()]

    @classmethod
    def get_description(cls, name):
        '''
        Метод возвращающий json-схему по имени поля БД: 
        {'column': 'Название', 'column_type': 'str'}
        '''
        return cls.get_json_schema()[name]

    #@classmethod
    #def get_type(cls, name):
        #'''Метод, по имени поля БД возвращающий тип данных колонки csv-файла'''
        #print(f"GET_TYPE:{cls.get_json_schema()}")
        #return cls.get_json_schema()[name]["column_type"]


class DownloadDataFromCsv:
    ''' Класс загрузки данных из csv-файла в БД '''

    REPLACENEMT = '["Общая"]'

    def __init__(self, obj: MuseumHeaders) -> None:
        self.obj = obj
        #self.title_list = obj.get_columns()
        self.df = pd.read_csv(LINK,  usecols=obj.get_columns(), sep=',')

    def prepare_data(self):
        for label, values in self.df.items():
            print(f"{label}: dtype={values.dtype}, non-null={values.notnull().sum()}")
            self.df[column] = np.where(
                pd.isnull(self.df[column]),
                replacement,
                self.df[column]
            )
        

    def prepare_column(self, field, replacement=REPLACENEMT):
        '''Метод подготовки данных в колонке csv-файла'''
        column, column_type  = self.obj.get_description(field).values()
        print(f"COLUMN:{column}, TYPE:{column_type}")
        self.df[column] = self.df[column].str.replace("&nbsp", replacement)
        self.df[column] = np.where(
            pd.isnull(self.df[column]),
            replacement,
            self.df[column]
            )
        print (f"PREPARE_LIST:{self.df[column]}")
        elem_list = []
        for row in self.df[column].values:
            print (f"PREPARE_ROW:{row}")
            if column_type == "dict":
                row = json.loads(row)
                elem_list.extend(row)
            if column_type == "str":
                elem_list.append(row)
        ready_list = list(set(elem_list))
        ready_list.sort()
        print (f"READY_LIST:{ready_list}")
        #return [{"category": ready_list}]

    # [' ', '(', ')', '-', '.', '–']

    def record_table(self, table: str, columns: List[Dict[str, list]]) -> None:
        for elem in columns:
            for key, value in elem.items():
                record = pd.DataFrame({key: value})
                record.to_sql(name=table, con=database.engine, if_exists='replace', index=False)

    

def parse_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line.strip()


def main(link):
    print(f"We are in main...")
    entries = parse_csv(link)
    idx = 0
    for entry in entries:
        print(entry)
        idx += 1
        if idx == 1:
            break

class PrepareUploadFile:
    pass



if __name__ == "__main__":
    #link="/home/vova/OpenData/Museums/data-20-structure-4.csv"
    #main(link)
    #to_dataframe(link)

    init = DownloadDataFromCsv(MuseumHeaders)

    data = init.prepare_data()
    print(f"DATA:{data}")

    #column = init.prepare_column("category")
    #print(f"COLUMN:{column}")

    #record = init.record_table("category", column)
    #print(f"RECORD:{record}")

    #location = init.prepare_column("location")
    #print(f"COLUMN:{location}")

    #teg = init.prepare_column("teg")
    #print(f"COLUMN:{teg}")
    
    '''
    init = MuseumHeaders()
    print(f"DUMP:{init.model_json_schema()}")
    elems = init.model_json_schema()
    for key, value in elems['properties'].items():
        print(f"ELEM:{key, value['default'], value['description']}")
    
    print(f"DATA:{MuseumHeaders.get_json_schema()}")
    print(f"COLUMNS:{MuseumHeaders.get_columns()}")
    print(f"COLUMNS:{MuseumHeaders.get_description('category')}")
    '''


    
