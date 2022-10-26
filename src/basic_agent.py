from player import Player


def get_first_unmortgaged(p_list):
    c = 0
    prop = p_list[c]
    while prop.is_mortgaged and c + 1 < len(p_list):
        c += 1
        prop = p_list[c]
    if prop.is_mortgaged:
        return None
    else:
        return prop


# RAISE MONEY SOMEHOW -------------- $
def raise_money(player: Player):
    l_imp, l_imp_prop = 100_000, None
    if "u" in player.owned:
        l_imp_prop = get_first_unmortgaged(player.owned["u"])
        if l_imp_prop:
            l_imp = l_imp_prop.price
            if player.check_monopoly("u"):
                l_imp = l_imp_prop.price * 2.0

    if "r" in player.owned:
        prop = get_first_unmortgaged(player.owned["r"])
        if prop and l_imp > prop.price * prop.multiplier:
            l_imp = prop.price * prop.multiplier
            l_imp_prop = prop

    for tier in range(8):
        if tier in player.owned:
            c_imp_prop = get_first_unmortgaged(player.owned[tier])
            if not c_imp_prop:
                continue
            c_imp = c_imp_prop.price
            if player.check_monopoly(c_imp_prop.color):
                c_imp = c_imp_prop.price * len(player.owned[c_imp_prop.color]) + sum(
                    [
                        prop.house_price * prop.buildings
                        for prop in player.owned[c_imp_prop.color]
                    ]
                )
            if c_imp < l_imp:
                l_imp = c_imp
                l_imp_prop = c_imp_prop
    player.mortgage(l_imp_prop)


# BUY OR NOT -------------- $
def buy_or_not(player: Player, property):
    if player.money >= property.price:
        player.buy(property, property.price)


# BUILD HOUSES OR NOT -------------- $
def build_or_not(player: Player):
    monopoly_tier = -1
    for t in reversed(range(8)):
        if player.check_monopoly(t):
            monopoly_tier = t
            break
    if monopoly_tier == -1:
        return
    monopoly_tier = player.owned[monopoly_tier]
    if player.money > 200.0:
        extra_money = player.money - 200.0
        num_buildings = int(extra_money // monopoly_tier[0].house_price)
        for building in range(num_buildings):
            monopoly_tier[
                len(monopoly_tier) - building % len(monopoly_tier) - 1
            ].make_building()
