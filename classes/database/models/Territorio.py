from ..DatabaseConnector import DatabaseConnector
from peewee import Model, CharField

connector = DatabaseConnector()

class Territorio(Model):
  nome = CharField()

  class Meta():
    database = connector.getDatabase()