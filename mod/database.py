from peewee import *

database = MySQLDatabase('shortlink', **{'host': '127.0.0.1', 'password': 'AlexprprHaoqiao', 'port': 3306, 'user': 'root'})

class BaseModel(Model):

    class Meta:
        database = database

class Pool(BaseModel):

    #data = TextField(null=False)
    time = DateTimeField(null=True)
    url = TextField(null=False)
    uid = TextField(null=False)
    title = TextField(null=False)
    content = TextField(null=False)
    #did = CharField(null=False)

    class Meta:
        db_table = 'pool'

class Record(BaseModel):

    time = DateTimeField(null=False)
    ip = TextField(null=False)
    ua = TextField(null=False)
    referer = TextField(null=False)

    class Meta:
        db_table = 'record'

if __name__ == '__main__':
    Pool.create_table(True)
    Record.create_table(True)