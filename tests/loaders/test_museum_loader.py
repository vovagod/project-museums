#import pytest
from tests.common import BASE_DIR
#from factory_museums import LocationFactory, CategoryFactory, MuseumFactory
from museums.loaders.museum_loader import DownloadDataFromCsv, SchemaConverter

LINK = BASE_DIR + "/data/data-20-structure-4-one.csv"

'''
def test_location_creation(session):
    #Sprint(f"SESSION: {session.__dict__}")  # development
    inst = LocationFactory()
    assert inst.location is not None
    assert isinstance(inst.location, str)
    #assert 0
    #assert isinstance(user.avatar, bytes)
    #assert user.location is not None
'''


def test_data_loading_proccess(test_engine, test_session, caplog):

    # инициализация
    init = DownloadDataFromCsv(SchemaConverter, LINK)
    # подготовка датафрейма
    data = init.prepare_data()
    # подготовка записей для таблицы Location
    location = init.prepare_unique_records("location")
    # перезапись колонки location в Museum как foreignkey к таблице Location
    init.prepare_foreignkey_column("location", location)
    # запись в таблицу Location
    record = init.record_table("locations", location, test_engine)
    # подготовка записей для таблицы Category
    category = init.prepare_unique_records("category")
    # запись в таблицу Category
    record = init.record_table("categories", category, test_engine)
    # переопределение колонки category в category_id в таблице Category
    init.redefine_column("category", "object")
    # запись в таблицу Museum
    record = init.record_table("museums", data, test_engine)
    for record in caplog.records:
        print(f"CAPLOG: {record.levelname}")
        assert record.levelname not in ["WARNING", "CRITICAL", "ERROR"]
