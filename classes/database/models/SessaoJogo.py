from ..DatabaseConnector import DatabaseConnector
from peewee import Model, CharField

connector = DatabaseConnector()

class SessaoJogo(Model):
  estadoPartida = CharField()

  class Meta():
    database = connector.getDatabase()