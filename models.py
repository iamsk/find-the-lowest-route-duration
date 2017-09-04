import datetime
from peewee import *

db = SqliteDatabase('duration.db')


class Duration(Model):
    origin = CharField()
    destination = CharField()
    date = DateField(default=datetime.date.today)
    hour = IntegerField()
    minute = IntegerField()
    duration = IntegerField()

    class Meta:
        database = db


if __name__ == '__main__':
    db.connect()
    db.create_tables([Duration])
