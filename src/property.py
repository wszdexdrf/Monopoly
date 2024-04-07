class Property:
    def __init__(self, price, color, rents) -> None:
        self.price = price
        self.color = color
        self.house_price = 50 * (color // 2 + 1)
        self.rent = rents
        self.mortgage_val = price / 2
        self.un_mortgage_val = self.mortgage_val * 1.1
        self.buildings = 0
        self.is_mortgaged = False
        self.owner = -1
        self.monopoly = False
        self.num_mortgaged_in_set = 0

    def get_owner(self):
        return self.owner

    def set_owner(self, new_owner):
        self.owner = new_owner

    def on_monopoly(self):
        self.monopoly = True

    def on_monopoly_lost(self):
        self.monopoly = False
    
    ### Track the number of mortgaged properties in the set. No houses can be built if any property in the set is mortgaged
    def some_mortgaged(self):
        self.num_mortgaged_in_set += 1

    def some_unmortgaged(self):
        self.num_mortgaged_in_set -= 1

    def get_rent(self, moves):
        if self.is_mortgaged:
            return 0
        if self.buildings == 0 and self.monopoly:
            return self.rent[0] * 2
        else:
            return self.rent[self.buildings]

    def make_building(self):
        if self.buildings < 5 and self.monopoly and self.num_mortgaged_in_set == 0:
            self.buildings += 1
            return self.house_price
        else:
            return -1

    def destroy_building(self):
        if self.buildings > 0:
            self.buildings -= 1
            return self.house_price / 2
        else:
            return -1

    def mortgage(self):
        if not self.is_mortgaged:
            self.is_mortgaged = True
            return self.mortgage_val
        else:
            return -1

    def un_mortgage(self):
        if self.is_mortgaged:
            self.is_mortgaged = False
            return self.un_mortgage_val
        else:
            return -1
