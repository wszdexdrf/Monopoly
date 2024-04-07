class Utility:
    def __init__(self) -> None:
        self.price = 150.0
        self.color = "u"
        self.mortgage_val = self.price / 2
        self.un_mortgage_val = self.mortgage_val * 1.1
        self.is_mortgaged = False
        self.owner = -1
        self.multiplier = 4

    def get_owner(self):
        return self.owner
    
    def some_mortgaged(self):
        pass

    def some_unmortgaged(self):
        pass

    def set_owner(self, new_owner):
        self.owner = new_owner

    # Utility rent becomes 10x the dice value when both utilities are owned
    def on_monopoly(self):
        self.multiplier = 10

    def on_monopoly_lost(self):
        self.multiplier = 4

    def get_rent(self, moves):
        if self.is_mortgaged:
            return 0
        return self.multiplier * moves

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
