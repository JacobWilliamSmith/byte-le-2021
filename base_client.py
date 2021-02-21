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
         # Get active contract
            # Set fuel sunk costs to 0
            # Set repair sunk costs to 0

        else:
            # variable to track money for upgrades
            # piggyBank = truck.money - (fuel sunk costs + repair sunk costs + 2 * ((avg * (fuel remaining)) + repair remaining costs))

            #check if tires are upgraded
            # if(TireType != "tire_econ" and piggybank >= 300):
            #     actions.set_action(ActionType.change_tires, TireType.tire_econ)change_tires
            
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