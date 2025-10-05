import random
from game.utils import slow_print

def start_battle(player, monster):
    slow_print(f"\n⚔️ A wild {monster.name} (Lv.{monster.level}) appears!")
    # reset defending flag
    player.defending = False

    while monster.hp > 0 and player.hp > 0:
        print(f"\n❤️ {player.name}: {player.hp}/{player.max_hp} HP | 🐉 {monster.name}: {monster.hp} HP")
        print("\n1. Normal Attack\n2. Heavy Attack\n3. Defend\n4. Use Item\n5. Run")
        choice = input("> ")

        player.defending = False  # reset each turn unless choose defend

        if choice == "1":
            dmg = player.attack("normal")
            monster.hp -= dmg
            slow_print(f"You hit {monster.name} for {dmg} damage!")

        elif choice == "2":
            dmg = player.attack("heavy")
            if dmg == 0:
                slow_print("You missed your heavy attack!")
            else:
                monster.hp -= dmg
                slow_print(f"Heavy hit! You dealt {dmg} damage!")

        elif choice == "3":
            player.defending = True
            slow_print("You brace yourself to defend. Incoming damage will be reduced.")

        elif choice == "4":
            if not player.inventory:
                print("You have no items!")
            else:
                for i, item in enumerate(player.inventory):
                    print(f"{i+1}. {item['name']}")
                idx = int(input("Choose item: ")) - 1
                player.use_item(idx)

        elif choice == "5":
            if random.random() < 0.5:
                slow_print("You successfully ran away!")
                return
            else:
                slow_print("You failed to escape!")

        # Monster turn (if alive)
        if monster.hp > 0:
            dmg = monster.attack()
            actual = player.take_damage(dmg)
            slow_print(f"{monster.name} hits you for {actual} damage!")

    if player.hp <= 0:
        slow_print("\n💀 You have been defeated...")
        player.hp = player.max_hp
    else:
        slow_print(f"\n🏆 You defeated {monster.name}!")
        player.gold += monster.gold_reward
        player.gain_exp(monster.exp_reward)
        print(f"💰 +{monster.gold_reward} gold | ⭐ +{monster.exp_reward} EXP")
        # update quests (kill quests)
        updated = player.update_quests_on_kill(monster)
        if updated:
            slow_print("You made progress on your quests!")
