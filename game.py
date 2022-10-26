from utility import Utility
from railroads import Railroad
from property import Property
from player import Player
import random
import basic_agent
import time

# Function to create a list of one color of properties and append
# it to a given list. The properties always have one lower price
# and the last one is of higher price. Similarly for rent.
def create_properties(
    list_to_append,
    color,
    low_price,
    high_price,
    num_properties,
    low_rents,
    high_rents,
):
    list_props = []
    for _ in range(1, num_properties):
        list_props.append(Property(low_price, color, low_rents))
    list_props.append(Property(high_price, color, high_rents))
    list_to_append.append(list_props)


# List of rents on all properties.
rents = [
    [2, 10, 30, 90, 160, 250],
    [4, 20, 60, 180, 320, 450],
    [6, 30, 90, 270, 400, 550],
    [8, 40, 100, 300, 450, 600],
    [10, 50, 150, 450, 625, 750],
    [12, 60, 180, 500, 700, 900],
    [14, 70, 200, 550, 750, 950],
    [16, 80, 220, 600, 800, 1000],
    [18, 90, 250, 700, 875, 1050],
    [20, 100, 300, 750, 925, 1100],
    [22, 110, 330, 800, 975, 1150],
    [24, 120, 360, 850, 1025, 1200],
    [26, 130, 390, 900, 1100, 1275],
    [28, 150, 450, 1000, 1200, 1400],
    [35, 175, 500, 1100, 1300, 1500],
    [50, 200, 600, 1400, 1700, 2000],
]

# One Game Instance
class Game:
    def __init__(self, num_players) -> None:
        # List of Colors of properties. (List of List of properties)
        self.properties = []
        # First brown set
        create_properties(self.properties, 0, 60.0, 60.0, 2, rents[0], rents[1])
        for c in range(1, 7):
            create_properties(
                self.properties,
                c,
                60.0 + c * 40.0,
                80.0 + c * 40.0,
                3,
                rents[c * 2],
                rents[c * 2 + 1],
            )
        # Final Indigo set
        create_properties(self.properties, 7, 350.0, 400.0, 2, rents[14], rents[15])

        # List of Railroads. All are identical.
        self.railroads = []
        for _ in range(4):
            self.railroads.append(Railroad())

        # List of Utilities
        self.utilities = [Utility(), Utility()]

        # The Board. Stores indices of properties etc.
        self.map = [0] * 40

        # Brown set
        self.map[0] = self.properties[0][0]
        self.map[2] = self.properties[0][1]
        for (i, tier) in enumerate(self.properties[1:-1]):
            self.map[(i + 1) * 5] = tier[0]
            self.map[(i + 1) * 5 + 2] = tier[1]
            self.map[(i + 1) * 5 + 3] = tier[2]
        # Indigo set
        self.map[36] = self.properties[7][0]
        self.map[38] = self.properties[7][1]

        # Railroads
        for i in range(4):
            self.map[i * 10 + 4] = self.railroads[i]

        # Utilities
        self.map[11] = self.utilities[0]
        self.map[27] = self.utilities[1]

        self.map[3] = 200
        self.map[37] = 100

        self.players = [Player(1500.0) for _ in range(num_players)]
        random.seed()

    def roll_die():
        return random.randint(1, 6) + random.randint(1, 6)

    def play(self):
        random.shuffle(self.players)
        limit = 10_000
        for i in range(limit):
            for player in self.players:
                die_val = Game.roll_die()
                location = player.move(die_val)
                if isinstance(self.map[location], int):
                    rent_received = player.pay_rent(self.map[location])
                    while rent_received == None:
                        basic_agent.raise_money(player)
                        rent_received = player.pay_rent(self.map[location])

                    if rent_received != self.map[location]:
                        player.defeated_to_bank()
                        self.players.remove(player)
                        continue

                elif self.map[location].owner == -1:
                    basic_agent.buy_or_not(player, self.map[location])

                elif self.map[location].get_owner() != player:
                    rent = self.map[location].get_rent(die_val)
                    rent_received = player.pay_rent(rent)
                    while rent_received == None:
                        basic_agent.raise_money(player)
                        rent_received = player.pay_rent(rent)

                    if rent_received != rent:
                        player.defeated(self.map[location].get_owner())
                        self.players.remove(player)
                        continue

                basic_agent.build_or_not(player)
                # TRADE OR NOT -------------- !
                # print(location, player.money)

            if len(self.players) == 1:
                # print (self.players[0], "WINS!!!")
                return i
            # print()
        return 0


if __name__ == "__main__":
    t_s = time.time()
    times = []
    g_won = 0

    for _ in range(100):
        t_b = time.time()
        g_won += Game(4).play()
        times.append(time.time() - t_b)

    # times.sort()
    avg = sum(times) / 100.0
    # 43.971
    print("Average number of moves per game", g_won / 100)
    print("Average time per game", avg)
    print("Total Time", time.time() - t_s)
