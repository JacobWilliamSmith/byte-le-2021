from game.client.user_client import UserClient
from game.common.enums import *


class Client(UserClient):
    # Variables and info you want to save between turns go here
    def __init__(self):
        super().__init__()
        self.turn = 0

    def team_name(self):
        """
        Allows the team to set a team name.
        :return: Your team name
        """
        return 'Team Name'

    # This is where your AI will decide what to do
    def take_turn(self, turn, actions, world, truck, time):
        """
        This is where your AI will decide what to do.
        :param turn:        The current turn of the game.
        :param actions:     This is the actions object that you will add effort allocations or decrees to.
        :param world:       Generic world information
        """
        self.turn += 1

        chosen_upgrade = self.select_upgrade(actions, truck)

        
            # Get active contract
            # Set fuel sunk costs to 0
            # Set repair sunk costs to 0
            print("")
        elif:
            # piggyBank = money on hand - (fuel sunk costs + repair sunk costs + 2 * (fuel remaining costs + repair remaining costs))
            
            # If(Don't have good tires and piggybank affords good tires)
                # Buy good tires
            # Elif(RF is not max level & Can afford to upgrade RF & Level of RF <= Level of FT)
                # Upgrade Rabbits Foot
            # Elif(FT is not max level & Can afford to upgrade FT)
                # Upgrade Fuel Tank
            # Elif(Need gas to survive next jump & Money on hand > 0)
                # Buy Fuel
            # Elif(Need repair to survive next jump worst case scenario & Money on hand > 0)
                # Buy Repair
            # Else:
                # Drive on optimal road





        # # If there is not an active contract get one
        # if(truck.active_contract is None):
        #     #print("Select")
        #     chosen_contract = self.select_new_contract(actions, truck)
        #     actions.set_action(ActionType.select_contract, chosen_contract)
        # # Buy gas if below 20% and there is enough money to fill tank to full at max gas price
        # elif(truck.body.current_gas < .20 and truck.money > 100*truck.active_contract.game_map.current_node.gas_price):
        #     #print("Gas")
        #     actions.set_action(ActionType.buy_gas)
        # # If health is below max and have enough money to fully repair do so
        # elif truck.health < 100 and truck.money > 1000:
        #     #print("Heal")
        #     actions.set_action(ActionType.repair)
        # elif chosen_upgrade is not None:
        #     #print("Upgrade")
        #     actions.set_action(ActionType.upgrade, chosen_upgrade)
        # elif(truck.active_contract.game_map.current_node.next_node is not None):
        #     # Move to next node
        #     # Road can be selected by passing the index or road object
        #     # print("Move:")
        #     actions.set_action(ActionType.select_route, roads.pop(0))

        # pass
        print("")
    # These methods are not necessary, so feel free to modify or replace
    def select_new_contract(self, actions, truck):
        pay, cost, time, roadmap, expVal = 0, best
        for contract in truck.contract_list:
            try:
                if contract.level == 0:
                    pass
            except AttributeError as e:
                pass
            roadmap = self.generate_roadMap(contract)
            pay = contract.money_reward
            cost = self.calculate_cost(contract, truck, roadmap) * contract.difficulty
            time = calculate_time(contract, roadmap)
            if((pay - cost) / time) > expVal:
                expVal = (pay - cost) / time
                best = contract
        if best != None:
            return best

        for contract in truck.contract_list:
            roadmap = self.generate_roadMap(contract)
            pay = contract.money_reward
            cost = self.calculate_cost(contract, truck, roadmap) * contract.difficulty
            time = calculate_time(contract, roadmap)
            if((pay - cost) / time) > expVal:
                expVal = (pay - cost) / time
                best = contract

        return best

    #calculates time to completion
    def calculate_time(self, contract, roadmap):
        time, temp = contract.game_map.head
        for i in range(len(roadmap)):
            time += self.road_h(temp.roads[roadmap[i]])
            temp = temp.next_node
        return time

    #calculates the cost for a contract
    def calculate_cost(self, contract, truck, roadmap):
        current_fuel = truck.body.gas, cost = 0
        temp = contract.game_map.head
        expected_damage = 0.0
        repair_rate_sum = 0.0

        for jump in roadmap:
            fuel_used = temp.roads[jump].length / 6.0746
            if (current_fuel - fuel_used <= 0):
                cost += temp.gas_price*(1-current_fuel)*100
                current_fuel = truck.max_gas
            current_fuel -= fuel_used
            expected_damage += 15 # adjust this later
            repair_rate_sum = temp.repair_price
            temp = temp.next_node
        
        repair_rate_avg = repair_rate_sum / len(roadmap)
        repair_cost = expected_damage * repair_rate_avg
        
        cost += repair_cost
        
        return cost
            


    # Contract can be selected by passing the index or contract object
    def select_upgrade(self, actions, truck):
        target_body_upgrade = ObjectType.tank
        target_addons_upgrade = ObjectType.rabbitFoot
        if truck.body.level < 3 and truck.get_cost_of_upgrade(target_body_upgrade) < truck.money:
            chosen_upgrade = target_body_upgrade
        elif truck.addons.level < 3 and truck.get_cost_of_upgrade(target_addons_upgrade) < truck.money:
            chosen_upgrade = target_addons_upgrade
        else:
            chosen_upgrade = None
        return chosen_upgrade
    
    # Road can be selected by passing the index or road object
    def select_new_route(self, actions, truck):
        roads = truck.active_contract.game_map.current_node.roads
        preference = 10
        for road in roads:
            temp = self.road_h(road)
            if temp < preference:
                best_road = road
        return road

    # Heuristic Functions
    def road_h(self, r):
        safetyPenalty = {0: 0, 1: 0.1429, 2: 0.1429, 3: 0.0426, 4: 0.4799, 5: 0.5461, 6: 0.5461}
        timeToPass = (r.length / 55.0) + (r.length / 121.491598) + 2.2380361
        return timeToPass + safetyPenalty[r.road_type]

    def generate_roadMap(self, contract):
        temp = contract.game_map.current_node
        numNodes = 0

        while(temp is not None):
            numNodes += 1
            temp = temp.next_node

        roadMap = [0 for i in range(numNodes)]
        temp = contract.game_map.current_node

        for i in range(numNodes):
            optRoad = 0
            for j in range(len(temp.roads)):
                if self.road_h(temp.roads[optRoad]) > self.road_h(temp.roads[j]):
                    optRoad = j
            roadMap[i] = optRoad
            temp = temp.next_node

        return roadMap


