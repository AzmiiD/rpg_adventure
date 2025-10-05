from game.items import ITEMS
from game.equipment import EQUIPMENTS
from game.utils import slow_print

def enter_shop(player):
    slow_print("\n🛒 Welcome to the shop!")
    while True:
        print(f"\nYour gold: {player.gold}")
        print("1. Buy Consumables")
        print("2. Buy Equipment")
        print("3. Exit shop")
        choice = input("> ")
        if choice == "1":
            buy_consumable(player)
        elif choice == "2":
            buy_equipment(player)
        elif choice == "3":
            break
        else:
            print("Invalid.")

def buy_consumable(player):
    from game.items import ITEMS
    while True:
        print("\n-- Consumables --")
        for i, item in enumerate(ITEMS):
            print(f"{i+1}. {item['name']} - {item['price']} gold")
        print(f"{len(ITEMS)+1}. Back")
        c = input("> ")
        if c.isdigit():
            c = int(c)
            if 1 <= c <= len(ITEMS):
                it = ITEMS[c-1]
                if player.gold >= it["price"]:
                    player.gold -= it["price"]
                    player.add_item(it.copy())
                    slow_print(f"You bought {it['name']}!")
                else:
                    print("Not enough gold!")
            elif c == len(ITEMS)+1:
                break
        else:
            print("Invalid.")

def buy_equipment(player):
    from game.equipment import EQUIPMENTS
    while True:
        print("\n-- Equipment --")
        for i, eq in enumerate(EQUIPMENTS):
            price = eq.get("price", 0)
            print(f"{i+1}. {eq['name']} ({eq['slot']}) - {price} gold")
        print(f"{len(EQUIPMENTS)+1}. Back")
        c = input("> ")
        if c.isdigit():
            c = int(c)
            if 1 <= c <= len(EQUIPMENTS):
                eq = EQUIPMENTS[c-1]
                if player.gold >= eq["price"]:
                    player.gold -= eq["price"]
                    # store equipment dict into inventory (copy)
                    player.add_item(eq.copy())
                    slow_print(f"You bought {eq['name']}!")
                else:
                    print("Not enough gold!")
            elif c == len(EQUIPMENTS)+1:
                break
        else:
            print("Invalid.")
