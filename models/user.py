from decouple import config
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute


class User(Model):
    class Meta:
        table_name = config("SHARED_PASSWORDS_POOL")
    email = UnicodeAttribute(hash_key=True)
    password = UnicodeAttribute()
    id = UnicodeAttribute(range_key=True)
    password_value = UnicodeAttribute(null=True)
    is_password_protected = BooleanAttribute(null=True)
    password_protection_hash = UnicodeAttribute(null=True)
