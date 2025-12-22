import factory
from common import Session
from factory.alchemy import SQLAlchemyModelFactory

from museums.models.museum_tables import Category, Location, Museum


class LocationFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Location
        sqlalchemy_session = Session

    id = factory.Sequence(lambda n: n)
    location = factory.Sequence(lambda n: f'Локация_{n}')


class CategoryFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Category
        sqlalchemy_session = Session

    id = factory.Sequence(lambda n: n)
    category = factory.Sequence(lambda n: f"Категория_{n}")


class MuseumFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Museum
        sqlalchemy_session = Session

    id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: f"Имя_{n}")
    address = factory.Sequence(lambda n: f"Адрес_{n}")

    @factory.lazy_attribute
    def category_id(self):
        return ["Персональный, мемориальный"]
    location_id = factory.SubFactory(LocationFactory)
    entity = factory.Sequence(lambda n: f"Юридическое_лицо_{n}")
    inn = factory.Sequence(lambda n: f"{n}")
    affiliation = factory.Sequence(lambda n: f"Принадлежность_{n}")
    submission = factory.Sequence(lambda n: f"Подчинение_{n}")
    timezone = "Europe/Moscow"

    @factory.lazy_attribute
    def teg(self):
        return [{"name": "Доступная среда"}]
    description = "1 августа 1803 года первый провинциальный музей России открыл свои двери..."
    website = "http://museumpereslavl.ru"
    email = "navy-museum@mail.ru"
    eipsk = factory.Sequence(lambda n: f"{n}")

    def service_name(self):
        return [
            {
                "url": "https://www.culture.ru/institutes/11238/muzei-usadba-botik-petra-i",
                "serviceName": "Культура.рф"
            },
            {
                "url": "https://visityaroslavia.ru/places/742/muzei-usadba-botik-petra-i",
                "serviceName": "Культурный регион"
            },
        ]
    updated_at = "2025-11-18T09:59:49Z"
