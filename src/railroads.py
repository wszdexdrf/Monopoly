class Railroad:
    def __init__(self) -> None:
        self.price = 200.0
        self.color = 'r'
        self.rent = 25.0
        self.multiplier = 1
        self.mortgage_val = self.price / 2
        self.un_mortgage_val = self.mortgage_val * 1.1
        self.is_mortgaged = False
        self.owner = -1

    def get_owner(self):
        return self.owner

    def set_owner(self, new_owner):
        self.owner = new_owner

    # Railroad rent increases by 2x when another railroad is bought
    def on_another_bought(self):
        self.multiplier *= 2

    ### Railroads mortgaged don't have any special effects on other railroads
    def some_mortgaged(self):
        pass

    def some_unmortgaged(self):
        pass

    def on_monopoly_lost(self):
        self.multiplier = 1

    def get_rent(self, moves):
        if self.is_mortgaged:
            return 0
        return self.multiplier * self.rent

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