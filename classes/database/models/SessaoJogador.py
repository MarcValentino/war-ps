from classes.database.models.SessaoJogo import SessaoJogo
from ..DatabaseConnector import DatabaseConnector
from peewee import Model, CharField, IntegerField, BooleanField, ForeignKeyField
#from models.SessaoJogo import SessaoJogo

connector = DatabaseConnector()

class SessaoJogador(Model):
  estadoPartida = CharField(column_name='estadopartida')
  idJogador = IntegerField(column_name='idjogador')
  idSessao = ForeignKeyField(SessaoJogo, backref='jogadores', column_name='idsessao')
  vez = BooleanField()
  ehDono = BooleanField(column_name='ehdono')
  naPartida = BooleanField(column_name='napartida')
  ehIA = BooleanField(column_name='ehia')
  cor = CharField()

  class Meta():
    database = connector.getDatabase()