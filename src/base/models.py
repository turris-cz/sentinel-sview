from peewee import *


__all__ = [
    "Fwlogs",
    "MinipotFtp",
    "MinipotHttp",
    "MinipotSmtp",
    "MinipotTelnet"
]

database = SqliteDatabase('base.db')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Identity(BaseModel):
    device_token = CharField(null=True)
    id = UnknownField(null=True, primary_key=True)  # BIGSERIAL
    sn = CharField()

    class Meta:
        table_name = 'identity'
        indexes = (
            (('sn', 'device_token'), True),
        )

class Fwlogs(BaseModel):
    asn = IntegerField(null=True)
    country = CharField(null=True)
    id = UnknownField(null=True, primary_key=True)  # BIGSERIAL
    identity = ForeignKeyField(column_name='identity_id', field='id', model=Identity, null=True)
    ip = UnknownField()  # INET
    local_ip = UnknownField()  # INET
    local_ports = UnknownField(null=True)  # INTEGER[]
    packet_count = IntegerField()
    protocol = CharField()
    ts = BigIntegerField()

    class Meta:
        table_name = 'fwlogs'

class MinipotFtp(BaseModel):
    action = CharField()
    asn = IntegerField(null=True)
    country = CharField(null=True)
    id = UnknownField(null=True, primary_key=True)  # BIGSERIAL
    identity = ForeignKeyField(column_name='identity_id', field='id', model=Identity, null=True)
    ip = UnknownField()  # INET
    password = TextField(null=True)
    ts = BigIntegerField()
    username = TextField(null=True)

    class Meta:
        table_name = 'minipot_ftp'

class MinipotHttp(BaseModel):
    action = CharField()
    asn = IntegerField(null=True)
    country = CharField(null=True)
    id = UnknownField(null=True, primary_key=True)  # BIGSERIAL
    identity = ForeignKeyField(column_name='identity_id', field='id', model=Identity, null=True)
    ip = UnknownField()  # INET
    method = TextField(null=True)
    password = TextField(null=True)
    ts = BigIntegerField()
    url = TextField(null=True)
    user_agent = TextField(null=True)
    username = TextField(null=True)

    class Meta:
        table_name = 'minipot_http'

class MinipotSmtp(BaseModel):
    action = CharField()
    asn = IntegerField(null=True)
    country = CharField(null=True)
    id = UnknownField(null=True, primary_key=True)  # BIGSERIAL
    identity = ForeignKeyField(column_name='identity_id', field='id', model=Identity, null=True)
    ip = UnknownField()  # INET
    mechanism = CharField(null=True)
    password = TextField(null=True)
    ts = BigIntegerField()
    username = TextField(null=True)

    class Meta:
        table_name = 'minipot_smtp'

class MinipotTelnet(BaseModel):
    action = CharField()
    asn = IntegerField(null=True)
    country = CharField(null=True)
    id = UnknownField(null=True, primary_key=True)  # BIGSERIAL
    identity = ForeignKeyField(column_name='identity_id', field='id', model=Identity, null=True)
    ip = UnknownField()  # INET
    password = TextField(null=True)
    ts = BigIntegerField()
    username = TextField(null=True)

    class Meta:
        table_name = 'minipot_telnet'

