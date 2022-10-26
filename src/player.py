from property import Property


class Player:
    def __init__(self, money) -> None:
        self.owned = {}
        self.money = money
        self.net_worth = money
        self.location = -1

    def check_monopoly(self, tier):
        if tier == 0 or tier == 7 or tier == "u":
            if tier not in self.owned:
                return False
            return len(self.owned[tier]) == 2
        else:
            if tier not in self.owned:
                return False
            return len(self.owned[tier]) == 3

    def move(self, places):
        self.location += places
        if self.location >= 40:
            self.money += 200.0
        self.location %= 40
        return self.location

    def buy(self, property, price):
        self.money -= price
        property.set_owner(self)
        if property.color in self.owned:
            self.owned[property.color].append(property)
            self.owned[property.color].sort(key=lambda property: property.price)
            if property.color == "r":
                for p in self.owned["r"]:
                    p.on_another_bought()
            elif self.check_monopoly(property.color):
                for p in self.owned[property.color]:
                    p.on_monopoly()
        else:
            self.owned[property.color] = [property]
        self.net_worth = self.net_worth - price + (property.mortgage_val if not property.is_mortgaged else 0)

    def mortgage(self, property):
        val = property.mortgage()
        if val != -1:
            for p in self.owned[property.color]:
                p.some_mortgaged()
            self.money += val
            return True
        else:
            return False

    def unmortgage(self, property):
        val = property.un_mortgage()
        if val != -1:
            for p in self.owned[property.color]:
                p.some_unmortgaged()
            self.money -= val
            self.net_worth = (
                self.net_worth - property.un_mortgage_val + property.mortgage_val
            )
            return True
        else:
            return False

    def build(self, property: Property):
        val = property.make_building()
        if val != -1:
            self.money -= val
            self.net_worth = self.net_worth - property.house_price / 2
            return True
        else:
            return False

    def destroy(self, property: Property):
        val = property.destroy_building()
        if val != -1:
            self.money += val
            return True
        else:
            return False

    def pay_rent(self, rent):
        if self.money >= rent:
            self.money -= rent
            self.net_worth -= rent
            return rent
        elif self.net_worth >= rent:
            return None
        else:
            return self.money

    def defeated(self, other_player):
        for (_, v) in self.owned.items():
            for p in v:
                other_player.buy(p, 0)

    def defeated_to_bank(self):
        for (_, v) in self.owned.items():
            for p in v:
                p.owner = -1
                p.on_monopoly_lost()
                p.un_mortgage()
                if isinstance(p, Property):
                    p.num_mortgaged_in_set = 0
                    p.buildings = 0
