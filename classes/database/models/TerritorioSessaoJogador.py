from ..DatabaseConnector import DatabaseConnector
from peewee import Model, IntegerField, ForeignKeyField
from classes.database.models.SessaoJogador import SessaoJogador
from classes.database.models.Territorio import Territorio

connector = DatabaseConnector()

class TerritorioSessaoJogador(Model):
  idSessaoJogador = ForeignKeyField(SessaoJogador, backref='jogadorRelacionado', column_name='idsessaojogador')
  idTerritorio = ForeignKeyField(Territorio, backref='territorioRelacionado', column_name='idterritorio')
  contagemTropas = IntegerField(column_name='contagemtropas')

  class Meta():
    database = connector.getDatabase()