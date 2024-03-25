from classes.GameMap import *
from classes.Territory import *
from classes.Game import *
from classes.Player import *
from classes.Dealer import *
from random import randint


class IA():     # herda da classe player
  
    def set_border_countries(self, gameMap: GameMap, color: str):
        player_territories = self.set_bsrs_bsts(gameMap, color)
        result = list(filter(lambda x: x.bst != 0, player_territories))
        # print(f'BODERRR  ----  {result}')
        return result

    def sort_bsr_ascendant(self, gameMap: GameMap, color: str):
        player_territories = self.set_bsrs_bsts(gameMap, color)
        result = list(filter(lambda y: y.bsr < 0.6, sorted(list(filter(lambda x: x.numberOfTroops > 1, player_territories)), key=lambda country: country.bsr)))
        '''print('ORIGIN')
        for t in result:
            print(f'{t.name} e bsr {t.bsr}')'''
        return result

    def sort_bsr_descendant(self, gameMap: GameMap, color: str):
        player_territories = self.set_bsrs_bsts(gameMap, color)
        result = list(filter(lambda y: y.bsr > 0.8, sorted(player_territories, key=lambda country: country.bsr, reverse=True)))
        '''print('TARGET')
        for t in result:
            print(f'{t.name} e bsr {t.bsr}')'''
        return result

    def set_bsrs_bsts(self, gameMap: GameMap, color: str):
        player_territories = gameMap.getAllTerritoriesOfColors(color)
        for territory in player_territories:
            territory.set_bst(gameMap.territories)
            territory.set_bsr()
        return player_territories
       
    def initiation_attack(self, gameMap: GameMap, color: str):

        if len(gameMap.getAllTerritoriesOfColors(color)) > 0:
            player_territories = self.set_bsrs_bsts(gameMap, color)
            borderCountries = self.set_border_countries(gameMap, color)
            originCountries = []
            
                


            for country in borderCountries:
                # print(f'{country.name} tem {country.numberOfTroops} tropas e tem bsr igual a {country.bsr}')
                chance = randint(0,10)
                if chance > 7:
                    print('BEST ATTACK')
                    self.best_attack(country, gameMap)
                if country.bsr < 5.9:
                    originCountries.append(country)
            # return originCountries        USADO PROS TESTES UNITARIOS
            self.main_attack(originCountries, gameMap, color)
        
    def best_attack(self, country: Territory, gameMap: GameMap):
            targets = sorted(country.getHostileTerritoryNeighbours(gameMap.territories), key= lambda x: x.numberOfTroops)
            if len(targets) > 0:
                target = targets[0]
                losses = gameMap.attackEnemyTerritoryBlitz(country.id, target.id)

    def main_attack(self, originCountries: list[Territory], gameMap: GameMap, color: str):
        tries_left = 30 # pode ocorrer um territorio tem bsr menor do que o limite estabelecido, mas nao atacar pq tem menos tropas que o inimigo e ai entra num loop
        while originCountries and tries_left:
            country = originCountries.pop(0)
            targetCountries = sorted(country.getHostileTerritoryNeighbours(gameMap.territories), key= lambda x: x.numberOfTroops)
            for target in targetCountries:
                targetTroops = target.numberOfTroops # soh fiz isso pra comparacao com as perdas depois
                if targetTroops > country.numberOfTroops:
                    break
                losses = gameMap.attackEnemyTerritoryBlitz(country.id, target.id)
                # print(f'IA {self.color}: {country.name} atacou {target.name}\n')
                # if losses[1] == targetTroops:   # isso pode sair no final, se nao tiver esse print
                    # print(f'IA {self.color}: {country.name} conquistou {target.name}\n')
            
            player_territories = self.set_bsrs_bsts(gameMap, color)
            borderCountries = self.set_border_countries(gameMap, color)
            originCountries = []
            for country in borderCountries:
                # print(f'{country.name} tem {country.numberOfTroops} tropas e tem bsr igual a {country.bsr}')
                if country.bsr <= 3.0 and country.numberOfTroops > 1:
                    originCountries.append(country)
            tries_left = tries_left -1


    def supply(self, additionalTroops: int, gameMap: GameMap, color: str):    # objetivo é deixar a distribuicao de tropas nos territorios a mais equilibrada possivel
        if len(gameMap.getAllTerritoriesOfColors(color)) > 0:
            player_territories = self.set_bsrs_bsts(gameMap, color)
            border_countries = self.set_border_countries(gameMap, color)
            while additionalTroops > 0:
                player_territories = self.set_bsrs_bsts(gameMap, color)
                targetCountries = sorted(border_countries, key= lambda country: country.bsr, reverse=True) # ordenar pelos bsr mais altos
                # print(f'{targetCountries[0].name} tem {targetCountries[0].numberOfTroops} tropas e bsr igual a {targetCountries[0].bsr}\n')
                if len(targetCountries) > 0:
                    if targetCountries[0].gainTroops(1):
                        additionalTroops = additionalTroops -1
                        # print(f'IA {self.color}: {targetCountries[0].name} recebeu 1 tropa\n')
                else:
                    targetCountries = sorted(gameMap.getAllTerritoriesOfColors(color), key= lambda country: country.bsr, reverse=True)
                    if targetCountries[0].gainTroops(1):
                        additionalTroops = additionalTroops -1
                
        # return player_territories     USADO PROS TESTES UNITARIOS

    def move(self, gameMap: GameMap, color: str):
        if len(gameMap.getAllTerritoriesOfColors(color)) > 0:
            player_territories = self.set_bsrs_bsts(gameMap, color)
            innerCountries =  list(filter(lambda x: x.bst == 0, player_territories))
            originCountries = list(filter(lambda country: country.numberOfTroops > 1, innerCountries))
            
            while originCountries:
                origin = originCountries.pop(0)
                player_territories = self.set_bsrs_bsts(gameMap, color)
                targetCountries = sorted(self.set_border_countries(gameMap, color), key= lambda country: country.bsr, reverse=True)
                for target in targetCountries:
                    path = gameMap.moveTroopsBetweenFriendlyTerrirories(origin.id, target.id, (origin.numberOfTroops -1), True)      # ideia é mandar todas as tropas para o territorio que mais precisa
                    if path != []:
                        # print(f'IA {self.color}: {origin.name} moveu suas tropas para {target.name}')
                        break


            player_territories = self.set_bsrs_bsts(gameMap, color)
            # fazer a parte de movimentacao das tropas de territorios com bsr baixo para territorios com bsr alto
            originCountries = self.sort_bsr_ascendant(gameMap, color)
            targetCountries = self.sort_bsr_descendant(gameMap, color)

            while originCountries:
                origin = originCountries.pop(0)
                # print(f'origin {origin.name}')
                for target in targetCountries:
                    # print(f'target {target.name}')
                    path = gameMap.moveTroopsBetweenFriendlyTerrirories(origin.id, target.id, 1, True)
                    player_territories = self.set_bsrs_bsts(gameMap, color)
                    if path != []:
                        # print(f'IA {self.color}: {origin.name} moveu 1 tropa para {target.name}')
                        while (origin.bsr < 0.6 and origin.numberOfTroops > 1):
                            path = gameMap.moveTroopsBetweenFriendlyTerrirories(origin.id, target.id, 1, True)
                            player_territories = self.set_bsrs_bsts(gameMap, color)
                            # if path != []:
                                # print(f'IA {self.color}: {origin.name} moveu 1 tropa para {target.name}')
                        if origin.bsr > 0.6: # movimentacao 'prejudicou' a origem, deve retornar a tropa
                                gameMap.moveTroopsBetweenFriendlyTerrirories(target.id, origin.id, 1, True)
                                break

        # return player_territories     USADO PROS TESTES UNITARIOS