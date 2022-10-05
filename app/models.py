from tortoise.models import Model
from tortoise import fields

class Clan(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    tag = fields.CharField(max_length=255)


class Player(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    clan = fields.ForeignKeyField('models.Clan', related_name='players')


class Season(Model):
    id = fields.IntField(pk=True)
    start_date = fields.DatetimeField()
    end_date = fields.DatetimeField(null=True)


class Session(Model):
    id = fields.IntField(pk=True)
    season = fields.ForeignKeyField('models.Season', related_name='sessions')
    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField(null=True)

class Checkin(Model):
    id = fields.IntField(pk=True)
    session = fields.ForeignKeyField('models.Session', related_name='checkins')
    player = fields.ForeignKeyField('models.Player', related_name='checkins')

class Points(Model):
    id = fields.IntField(pk=True)
    player = fields.ForeignKeyField('models.Player', related_name='points')
    season = fields.ForeignKeyField('models.Season', related_name='points')
    clan = fields.ForeignKeyField('models.Clan', related_name='points')
    points = fields.IntField(default=0)