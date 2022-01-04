from faker import Factory, Faker

from db import db
from models import CreatorModel, SecretModel


class BaseFactory(Factory):
    @classmethod
    def create(cls, **kwargs):
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.flush()
        return object


class CreatorFactory(BaseFactory):
    class Meta:
        model = CreatorModel

    fake = Faker()
    email = fake.email()
    password = fake.password()


class SecretFactory(BaseFactory):
    class Meta:
        model = SecretModel

    fake = Faker()
    secret = fake.password()
    password = fake.password()
    creator_id = 1
