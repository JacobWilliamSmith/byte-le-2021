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
        roads = []
        if(truck.active_contract is not None):
            roads = self.generateRoadMap(truck)

        chosen_upgrade = self.select_upgrade(actions, truck)
        # If there is not an active contract get one
        if(truck.active_contract is None):
            #print("Select")
            chosen_contract = self.select_new_contract(actions, truck)
            actions.set_action(ActionType.select_contract, chosen_contract)
        # elif(truck.body.TireType != 1):
        #     self.select_new_tires(actions, truck, "tire_econ")
        # Buy gas if below 20% and there is enough money to fill tank to full at max gas price
        elif(truck.body.current_gas < .20 and truck.money > 100*truck.active_contract.game_map.current_node.gas_price):
            #print("Gas")
            actions.set_action(ActionType.buy_gas)
        # If health is below max and have enough money to fully repair do so
        elif truck.health < 100 and truck.money > 1000:
            #print("Heal")
            actions.set_action(ActionType.repair)
        elif chosen_upgrade is not None:
            #print("Upgrade")
            actions.set_action(ActionType.upgrade, chosen_upgrade)
        elif(truck.active_contract.game_map.current_node.next_node is not None):
            # Move to next node
            # Road can be selected by passing the index or road object
            # print("Move:")
            actions.set_action(ActionType.select_route, roads.pop(0))
        
        pass

    # These methods are not necessary, so feel free to modify or replace
    def select_new_contract(self, actions, truck):
        selected_contract = truck.contract_list[0]
        for contract in truck.contract_list:
            try:
                if(contract.level == 0 ):
                    print("illegal contact")
            except AttributeError as e:
                # print("legal contract")
                if(contract.difficulty == "easy"):
                    selected_contract = contract
        return selected_contract

    def select_new_tires(self, actions, truck, tireType):
        print("switched tires")
        actions.set_action(ActionType.change_tires, TireType.tireType)

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
    

    # Heuristic Functions
    def road_h(self, r):
        safetyPenalty = {0: 0, 1: 0.1429, 2: 0.1429, 3: 0.0426, 4: 0.4799, 5: 0.5461, 6: 0.5461}
        timeToPass = (r.length / 55.0) + (r.length / 121.491598) + 2.2380361
        return timeToPass + safetyPenalty[r.road_type]

    def generateRoadMap(self, truck):
        temp = truck.active_contract.game_map.current_node
        numNodes = 0

        while(temp is not None):
            numNodes += 1
            temp = temp.next_node

        roadMap = [0 for i in range(numNodes)]
        temp = truck.active_contract.game_map.current_node

        for i in range(numNodes):
            optRoad = 0
            for j in range(len(temp.roads)):
                if self.road_h(temp.roads[optRoad]) > self.road_h(temp.roads[j]):
                    optRoad = j
            roadMap[i] = optRoad
            temp = temp.next_node

        return roadMap