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
        self.turn += 1


        
        # Get active contract
        # Set fuel sunk costs to 0
        # Set repair sunk costs to 0
        
        # If there is not an active contract get one
        if(truck.active_contract is None):
            chosen_contract = self.select_new_contract(actions, truck)
            actions.set_action(ActionType.select_contract, chosen_contract)
        else:
            piggyBank = truck.money - self.calculate_cost(truck.active_contract, truck, self.generate_roadMap(truck.active_contract))

            if 0: 
            
            elif(truck.money > 300 and truck.tires != 1):
	        print(truck.tires)
	        actions.set_action(ActionType.change_tires, TireType.tire_econ)

            elif(truck.active_contract.game_map.current_node.next_node is not None):
                print("Move:")
                optRoad = 0

                for i in range(len(temp.roads)):
                    if self.road_h(temp.roads[optRoad]) > self.road_h(temp.roads[i]):
                        optRoad = i

                r = roads[optRoad]
                fuel_used = r.length / 6.0746
                worstCaseHPLoss = {0: 0, 1: 34.28, 2: 34.28, 3: 31.16, 4: 48, 5: 20.51, 6: 20.51}
                hp_used = worstCaseHPLoss[r.road_type] # Todo: Deduct rabbit foot protection

                if current_fuel - fuel_used <= 0 and truck.money > 0:
                    actions.set_action(ActionType.buy_gas)
                elif truck.health - hp_used <= 0 and truck.money > 0:
                    actions.set_action(ActionType.repair)
                else:
                    actions.set_action(ActionType.select_route, r)

        pass

            # variable to track money for upgrades
            # piggyBank = truck.money - (fuel sunk costs + repair sunk costs + 2 * ((avg * (fuel remaining)) + repair remaining costs))

            #check if tires are upgraded
            # if(bool(TireType.tire_econ) and piggybank >= 300):
            #     actions.set_action(ActionType.change_tires, TireType.tire_econ)
            
            #upgrades rabbit's foot if the level is less than or equal to the tank level and there is piggybank money for it
            # Elif(truck.addons.level < 3 and truck.get_cost_of_upgrade(target_addons_upgrade) < piggybank and truck.addons.level <= truck.body.level)
                #actions.set_action(ActionType.upgrade, ObjectType.rabbitFoot)
            
            #upgrades fuel tank if there is piggy bank money for it
            # Elif(truck.body.level < 3 and truck.get_cost_of_upgrade(target_body_upgrade) < piggybank)
                #actions.set_action(ActionType.upgrade, ObjectType.tank)

            # checks if gas is necessary
            # Elif(need gas to survive and truck.money > 0)
                # actions.set_action(ActionType.buy_gas)
            
            #checks if repair is necessary
            # Elif(if truck.health <= 48 and truck.money > 0)
                # actions.set_action(ActionType.repair)
            
            #drives
            # Else:
                # Drive on optimal road



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