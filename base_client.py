from game.client.user_client import UserClient
from game.common.enums import *


class Client(UserClient):
    # Variables and info you want to save between turns go here
    def __init__(self):
        super().__init__()
        self.turn = 0
        self.roads = []

    def team_name(self):
        """
        Allows the team to set a team name.
        :return: Your team name
        """
        return 'piston_cup_champions'

    # This is where your AI will decide what to do
    def take_turn(self, turn, actions, world, truck, time):
        self.turn += 1
        chosen_upgrade = self.select_upgrade(actions, truck)

        if(truck.active_contract is None):
            contract = self.select_new_contract(actions, truck)
            self.roads = self.generate_roadMap(contract)
            actions.set_action(ActionType.select_contract, contract)
        elif truck.speed is not 55:
            actions.set_action(ActionType.set_speed, 55)
        elif truck.tires != 1:
            actions.set_action(ActionType.change_tires, TireType.tire_econ)
        elif(truck.health < 50):
            actions.set_action(ActionType.repair)
        elif(truck.body.current_gas < .20 and truck.money > 100*truck.active_contract.game_map.current_node.gas_price):
            actions.set_action(ActionType.buy_gas)
        elif(truck.active_contract.game_map.current_node.next_node is not None):
            actions.set_action(ActionType.select_route, self.roads.pop(0))
        pass
    def select_new_contract(self, actions, truck):
        pay = 0
        cost = 0
        time = 0
        roadmap = None
        expVal = 0
        best = None
        for contract in truck.contract_list:
            try:
                if contract.level == 0:
                    pass
            except AttributeError as e:
                roadmap = self.generate_roadMap(contract)
                pay = contract.money_reward
                cost = self.calculate_cost(contract, truck, roadmap) * contract.difficulty
                time = self.calculate_time(contract, roadmap)
                if((pay - cost) / time) > expVal:
                    expVal = (pay - cost) / time
                    best = contract
            if best != None:
                return best

        for contract in truck.contract_list:
            roadmap = self.generate_roadMap(contract)
            pay = contract.money_reward
            cost = self.calculate_cost(contract, truck, roadmap) * contract.difficulty
            time = self.calculate_time(contract, roadmap)
            if((pay - cost) / time) > expVal:
                expVal = (pay - cost) / time
                best = contract

        return best

    #calculates time to completion
    def calculate_time(self, contract, roadmap):
        time = 0
        temp = contract.game_map.head
        for i in range(len(roadmap)):
            time += self.road_h(temp.roads[roadmap[i]])
            temp = temp.next_node
        return time

    #calculates the cost for a contract
    def calculate_cost(self, contract, truck, roadmap):
        current_fuel = truck.body.current_gas
        cost = 0
        counter = 0
        temp = contract.game_map.head
        expected_damage = 0.0
        repair_rate_sum = 0.0
        for jump in roadmap:
            fuel_used = temp.roads[jump].length / 6.0746
            if (current_fuel - fuel_used <= 0):
                cost += temp.gas_price*(1-current_fuel)*100
                current_fuel = truck.body.max_gas
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
        temp = contract.game_map.head
        numNodes = 0

        while(temp.next_node is not None):
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