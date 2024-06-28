from peewee import PostgresqlDatabase

DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_HOST = 'localhost'
DB_PORT = 5432

class DatabaseConnector(object):
  _instance = None

  def __new__(self):
    if self._instance is None:
      self._instance = super().__new__(self)
      self._instance.db = PostgresqlDatabase(DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    return self._instance

  def getDatabase(self):
    return self.db
