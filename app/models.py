from tortoise import fields, timezone
from tortoise.expressions import Q
from tortoise.fields import ForeignKeyNullableRelation, ForeignKeyRelation
from tortoise.manager import Manager
from tortoise.models import Model
from tortoise.queryset import QuerySet


class Channel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    discord_server_id = fields.CharField(max_length=255, unique=True, null=True)

class Clan(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=False)
    tag = fields.CharField(max_length=4, unique=False)
    channel = fields.ForeignKeyField("models.Channel", related_name="clans")


class StatusManager(Manager):
    def get_queryset(self) -> QuerySet["Player"]:
        return super(StatusManager, self).get_queryset().filter(enabled=True)


class Player(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=False)
    clan: ForeignKeyNullableRelation[Clan] = fields.ForeignKeyField(
        "models.Clan", related_name="players", null=True
    )
    channel = fields.ForeignKeyField("models.Channel", related_name="players")
    enabled = fields.BooleanField(default=True)

    enabled_players = StatusManager()

    def is_enabled(self) -> bool:
        return self.enabled


class SeasonActiveManager(Manager):
    def get_queryset(self) -> QuerySet["Season"]:
        return (
            super(SeasonActiveManager, self)
            .get_queryset()
            .filter(
                Q(start_date__lte=timezone.now()),
                Q(end_date__gte=timezone.now())
                | Q(end_date__isnull=True) & Q(start_date__lte=timezone.now()),
            )
        )


class PreviousSeasonsManager(Manager):
    def get_queryset(self) -> QuerySet["Season"]:
        return (
            super(PreviousSeasonsManager, self)
            .get_queryset()
            .filter(Q(start_date__lte=timezone.now()), Q(end_date__lte=timezone.now()))
        )


class Season(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=False)
    start_date = fields.DatetimeField(auto_now_add=True)
    end_date = fields.DatetimeField(null=True)
    info_end_date = fields.DatetimeField(null=True)
    channel = fields.ForeignKeyField("models.Channel", related_name="seasons")

    active_seasons = SeasonActiveManager()
    previous_seasons = PreviousSeasonsManager()


class SessionActiveManager(Manager):
    def get_queryset(self) -> QuerySet["Session"]:
        return (
            super(SessionActiveManager, self)
            .get_queryset()
            .filter(
                Q(start_time__lte=timezone.now()),
                Q(end_time__gte=timezone.now())
                | Q(end_time__isnull=True) & Q(start_time__lte=timezone.now()),
            )
        )


class RaidSessionActiveManager(Manager):
    def get_queryset(self) -> QuerySet["RaidSession"]:
        return (
            super(RaidSessionActiveManager, self)
            .get_queryset()
            .filter(
                Q(start_time__lte=timezone.now()),
                Q(end_time__gte=timezone.now())
                | Q(end_time__isnull=True) & Q(start_time__lte=timezone.now()),
            )
        )


class Session(Model):
    id = fields.IntField(pk=True)
    season: ForeignKeyRelation[Season] = fields.ForeignKeyField(
        "models.Season", related_name="sessions"
    )
    start_time = fields.DatetimeField(auto_now_add=True)
    end_time = fields.DatetimeField(null=True)
    channel = fields.ForeignKeyField("models.Channel", related_name="sessions")

    active_session = SessionActiveManager()


class Checkin(Model):
    id = fields.IntField(pk=True)
    session: ForeignKeyRelation[Session] = fields.ForeignKeyField(
        "models.Session", related_name="checkins"
    )
    player: ForeignKeyRelation[Player] = fields.ForeignKeyField(
        "models.Player", related_name="checkins"
    )
    channel = fields.ForeignKeyField("models.Channel", related_name="checkins")


class RaidSession(Model):
    id = fields.IntField(pk=True)
    season: ForeignKeyRelation[Season] = fields.ForeignKeyField(
        "models.Season", related_name="raid_sessions"
    )
    start_time = fields.DatetimeField(auto_now_add=True)
    end_time = fields.DatetimeField(null=True)
    channel = fields.ForeignKeyField("models.Channel", related_name="raid_sessions")

    active_session = RaidSessionActiveManager()


class RaidCheckin(Model):
    id = fields.IntField(pk=True)
    session: ForeignKeyRelation[Session] = fields.ForeignKeyField(
        "models.RaidSession", related_name="raid_checkins"
    )
    player: ForeignKeyRelation[Player] = fields.ForeignKeyField(
        "models.Player", related_name="raid_checkins"
    )
    channel = fields.ForeignKeyField("models.Channel", related_name="raid_checkins")


class Points(Model):
    id = fields.IntField(pk=True)
    player: ForeignKeyRelation[Player] = fields.ForeignKeyField(
        "models.Player", related_name="points"
    )
    season: ForeignKeyRelation[Season] = fields.ForeignKeyField(
        "models.Season", related_name="points"
    )
    clan: ForeignKeyRelation[Clan] = fields.ForeignKeyField("models.Clan", related_name="points")
    channel = fields.ForeignKeyField("models.Channel", related_name="points")
    points = fields.IntField(default=0)


class EventSubscriptions(Model):
    id = fields.IntField(pk=True)
    channel_name = fields.CharField(max_length=255)
    event_type = fields.CharField(max_length=255)
    subscribed = fields.BooleanField()


class Subscriptions(Model):
    id = fields.IntField(pk=True)
    player: ForeignKeyRelation[Player] = fields.OneToOneField(
        "models.Player", related_name="subscriptions"
    )
    channel = fields.ForeignKeyField("models.Channel", related_name="subscriptions")
    months_subscribed = fields.IntField(default=1)
    currently_subscribed = fields.BooleanField()


class RewardLevel(Model):
    id = fields.IntField(pk=True)
    channel = fields.ForeignKeyField("models.Channel", related_name="reward_levels")
    level = fields.IntField(unique=True)
    reward = fields.CharField(max_length=255)