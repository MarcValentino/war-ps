import re
from classes.GameMap import *
from classes.Territory import *
from classes.Region import *
from classes.IA import *




# PARA FAZER OS TESTES, TEM QUE COLOCAR O ATRIBUTO COLOR EM TERRITORIO
# ACREDITO QUE DEPOIS DE INTEGRADO, VAI OCORRER NORMALMENTE



testTerritories: list[Territory] = [Territory([1, 2], 0, 'teste0', 0, 10, 10, 'azul'), Territory([0, 4], 0, 'teste1', 1, 10, 10, 'azul'), Territory([0, 3], 0, 'teste2', 2, 10, 10, 'branco'), Territory([2, 4, 5], 1, 'teste3', 3, 10, 10, 'branco'), Territory([3, 1], 1, 'teste4', 4, 10, 10, 'azul'), Territory([3], 0, 'teste5', 5, 10, 10, 'branco'), Territory([7], 2, 'teste6', 6, 10, 10, 'azul'), Territory([6], 2, 'teste7', 7, 10, 10, 'azul')]
testRegions: list[Region] = [Region('a', 3, 0), Region('b', 2, 1), Region('c', 2, 2)]
testMap = GameMap(testTerritories, testRegions)
ia1= IA(testMap, 1, 'ia1', 'azul')
ia2= IA(testMap, 2, 'ia2', 'branco')


'''
def test_ia_supply():
  print('SUPPLY')
  for territory in testTerritories:
      print(f'{territory.name} tem {territory.numberOfTroops} tropas\n')

  ia1.supply(5)

  for territory in testTerritories:
      print(f'{territory.name} tem {territory.numberOfTroops} tropas\n')


def test_ia_attack():

  print('ATTACK')
  print('===============================')

  ia1.initiation_attack()

  for territory in testTerritories:
      print(f'{territory.name} do IA {territory.color} tem {territory.numberOfTroops} tropas\n')

  print('===============================')



def test_ia_move():

  print('MOVE')
  print('===============================')

  ia1.move()

  for territory in testTerritories:
      print(f'{territory.name} do IA {territory.color} tem {territory.numberOfTroops} tropas\n')

  print('===============================')

result = ia1.getAllTerritoriesOfColors(testMap)
print(result)
test_ia_supply()
test_ia_attack()
test_ia_move()'''


'''
def test_get_territories():
  result = ia1.get_territories(testMap)
  oraculo = [Territory([1, 2], 0, 'teste0', 0, 10, 10, 'azul'), Territory([0, 4], 0, 'teste1', 1, 10, 10, 'azul'),Territory([3, 1], 1, 'teste4', 4, 10, 10, 'azul'),Territory([7], 2, 'teste6', 6, 10, 10, 'azul'), Territory([6], 2, 'teste7', 7, 10, 10, 'azul')]
  for i in range(len(oraculo)):
    assert result[i].name == oraculo[i].name


def test_set_bsr():
  terr = ia1.set_bsrs_bsts()
  oraculo = [1,0,1,0,0]
  for i in range(len(terr)):
    assert terr[i].bsr == oraculo[i]

def test_border_countries():
  result = ia1.set_border_countries()
  oraculo = [Territory([1, 2], 0, 'teste0', 0, 10, 10, 'azul'),Territory([3, 1], 1, 'teste4', 4, 10, 10, 'azul')]
  for i in range(len(oraculo)):
    assert result[i].name == oraculo[i].name

def test_bsr_asc():
  result = ia1.sort_bsr_ascendant()
  oraculo = [Territory([0, 4], 0, 'teste1', 1, 10, 10, 'azul'), Territory([7], 2, 'teste6', 6, 10, 10, 'azul'), Territory([6], 2, 'teste7', 7, 10, 10, 'azul')]
  for i in range(len(oraculo)):
    assert result[i].name == oraculo[i].name

def test_bsr_desc():
  result = ia1.sort_bsr_descendant()
  oraculo = [Territory([1, 2], 0, 'teste0', 0, 10, 10, 'azul'),Territory([3, 1], 1, 'teste4', 4, 10, 10, 'azul')]
  for i in range(len(oraculo)):
    assert result[i].name == oraculo[i].name


def test_supply():
  terr = ia1.supply(5)
  oraculo = [18,15,17,15,15]
  for i in range(len(terr)):
    assert terr[i].numberOfTroops == oraculo[i]



def test_move():
  terr = ia1.move()
  oraculo = [25,1,19,15,15]
  for i in range(len(terr)):
    assert terr[i].numberOfTroops == oraculo[i]


def test_init_atk():
  origin = ia1.initiation_attack()
  oraculo = [Territory([1, 2], 0, 'teste0', 0, 10, 10, 'azul'), Territory([3, 1], 1, 'teste4', 4, 10, 10, 'azul')]
  for i in range(len(oraculo)):
    assert origin[i].name == oraculo[i].name
'''





    

    







# SEGUNDO CENARIO DE TESTES    
        
testTerritories: list[Territory] = [Territory([1, 2], 0, 'teste0', 0, 10, 10, 'VERDE'), Territory([0, 4], 0, 'teste1', 1, 10, 10, 'VERDE'), Territory([0, 3, 4], 0, 'teste2', 2, 10, 10, 'PRETO'), Territory([2, 4, 5], 1, 'teste3', 3, 10, 10, 'PRETO'), Territory([3, 1, 2], 1, 'teste4', 4, 10, 10, 'VERDE'), Territory([3], 0, 'teste5', 5, 10, 10, 'PRETO'), Territory([7], 2, 'teste6', 6, 10, 10, 'VERDE'), Territory([6], 2, 'teste7', 7, 10, 10, 'VERDE')]
testRegions: list[Region] = [Region('a', 3, 0), Region('b', 2, 1), Region('c', 2, 2)]
testMap = GameMap(testTerritories, testRegions)
ia3= IA(testMap, 1, 'ia3', 'VERDE')
ia4= IA(testMap, 2, 'ia4', 'PRETO')


'''
def test_ia_supply():
  print('SUPPLY')
  for territory in testTerritories:
      print(f'{territory.name} tem {territory.numberOfTroops} tropas\n')

  ia1.supply(5)

  for territory in testTerritories:
      print(f'{territory.name} tem {territory.numberOfTroops} tropas\n')


def test_ia_attack():

  print('ATTACK')
  print('===============================')

  ia1.initiation_attack()

  for territory in testTerritories:
      print(f'{territory.name} do IA {territory.color} tem {territory.numberOfTroops} tropas\n')

  print('===============================')



def test_ia_move():

  print('MOVE')
  print('===============================')

  ia1.move()

  for territory in testTerritories:
      print(f'{territory.name} do IA {territory.color} tem {territory.numberOfTroops} tropas\n')

  print('===============================')

result = ia1.get_territories(testMap)
print(result)
test_ia_supply()
test_ia_attack()
test_ia_move()'''

def test_get_territories():
  result = ia3.get_territories(testMap)
  oraculo = [Territory([1, 2], 0, 'teste0', 0, 10, 10, 'VERDE'), Territory([0, 4], 0, 'teste1', 1, 10, 10, 'VERDE'), Territory([3, 1, 2], 1, 'teste4', 4, 10, 10, 'VERDE'), Territory([7], 2, 'teste6', 6, 10, 10, 'VERDE'), Territory([6], 2, 'teste7', 7, 10, 10, 'VERDE')]
  for i in range(len(oraculo)):
    assert result[i].name == oraculo[i].name


def test_set_bsr():
  terr = ia3.set_bsrs_bsts()
  oraculo = [1,0,2,0,0]
  for i in range(len(terr)):
    assert terr[i].bsr == oraculo[i]

def test_border_countries():
  result = ia3.set_border_countries()
  oraculo = [Territory([1, 2], 0, 'teste0', 0, 10, 10, 'VERDE'), Territory([3, 1, 2], 1, 'teste4', 4, 10, 10, 'VERDE')]
  for i in range(len(oraculo)):
    assert result[i].name == oraculo[i].name

def test_bsr_asc():
  result = ia3.sort_bsr_ascendant()
  oraculo = [Territory([0, 4], 0, 'teste1', 1, 10, 10, 'VERDE'),Territory([7], 2, 'teste6', 6, 10, 10, 'VERDE'), Territory([6], 2, 'teste7', 7, 10, 10, 'VERDE')]
  for i in range(len(oraculo)):
    assert result[i].name == oraculo[i].name

def test_bsr_desc():
  result = ia1.sort_bsr_descendant()
  oraculo = [Territory([1, 2], 0, 'teste0', 0, 10, 10, 'VERDE'), Territory([3, 1, 2], 1, 'teste4', 4, 10, 10, 'VERDE')]
  for i in range(len(oraculo)):
    assert result[i].name == oraculo[i].name

'''
def test_supply():
  terr = ia3.supply(5)
  oraculo = [15,15,20,15,15]
  for i in range(len(terr)):
    assert terr[i].numberOfTroops == oraculo[i]
'''

'''
def test_move():
  terr = ia3.move()
  oraculo = [15,1,29,15,15]
  for i in range(len(terr)):
    assert terr[i].numberOfTroops == oraculo[i]
'''

def test_init_atk():
  origin = ia3.initiation_attack()
  oraculo = [Territory([1, 2], 0, 'teste0', 0, 10, 10, 'VERDE')]
  for i in range(len(oraculo)):
    assert origin[i].name == oraculo[i].name

