from peewee import *


db = PostgresqlDatabase(database='lesson13', user='postgres', password='Jiga057096')

class BaseModel(Model):

    class Meta:
        databases = db


class UnsignetIntegerField(IntegerField):
    field_type = 'int unsigned'

class Users(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=150, null=False, constraints=[Check('name!=""')])
    age = UnsignetIntegerField(constraints=[Check('age>0 and age < 130')])
    gender = CharField(max_length=10, null=False)
    nationality = CharField(max_length=50)


class Posts(BaseModel):
    id = PrimaryKeyField()
    user_id = ForeignKeyField(Users, on_delete='set null')
    title = CharField(max_length=100, default='Заголовок не указан')
    description = TextField()


class Likes(BaseModel):
    id = PrimaryKeyField()
    user_id = ForeignKeyField(Users, on_delete='set null')
    post_id = ForeignKeyField(Posts, on_delete='set null')


class Comments(BaseModel):
    id = PrimaryKeyField()
    text_ = TextField()
    user_id = ForeignKeyField(Users, on_delete='set null')
    post_id = ForeignKeyField(Posts, on_delete='set null')

