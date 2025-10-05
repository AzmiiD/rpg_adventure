from game.player import Player
from game.monster import Monster
from game.battle import start_battle
from game.shop import enter_shop
from game.save_manager import save_game, load_game
from game.utils import clear_screen, slow_print, loading_bar, Color
from game.npc import NPC
from game.quest import SAMPLE_QUESTS


def show_status(player):
    print(f"\n👤 {player.name} | ❤️ {player.hp}/{player.max_hp} | 💰 {player.gold} | 🧭 Level {player.level} | EXP {player.exp}")


def inventory_menu(player):
    while True:
        print("\n-- Inventory --")
        if not player.inventory:
            print("Empty.")
        else:
            for i, it in enumerate(player.inventory):
                slot = it.get("slot", "")
                extra = f" ({slot})" if slot else ""
                print(f"{i+1}. {it['name']}{extra}")

        print("a. Equip item from inventory")
        print("u. Unequip (weapon/armor)")
        print("b. Back")
        c = input("> ").strip().lower()

        if c == "a":
            choice = input("Inventory index to equip: ").strip()
            if not choice.isdigit():
                print("❌ Invalid input. Please enter a number.")
                continue
            idx = int(choice) - 1
            if idx < 0 or idx >= len(player.inventory):
                print("❌ Invalid index.")
                continue
            player.equip_from_inventory(idx)

        elif c == "u":
            slot = input("Which slot to unequip? (weapon/armor) > ").strip().lower()
            if slot not in ["weapon", "armor"]:
                print("❌ Invalid slot name.")
                continue
            player.unequip(slot)

        elif c == "b":
            break
        else:
            print("❌ Invalid choice.")


def town_menu(player):
    npc = NPC("Elder", quests=SAMPLE_QUESTS)
    npc.talk(player)


def main_menu(player):
    while True:
        clear_screen()
        show_status(player)
        print("\n🏙️  Where do you want to go?")
        print("1. ⚔️  Arena (Battle)")
        print("2. 🏪 Shop")
        print("3. 🧙 Town (NPCs & Quests)")
        print("4. 🎒 Inventory / Equip")
        print("5. 💾 Save Game")
        print("6. 🚪 Exit")

        choice = input("> ").strip()

        if choice == "1":
            monster = Monster(player.level)
            start_battle(player, monster)
        elif choice == "2":
            enter_shop(player)
        elif choice == "3":
            town_menu(player)
        elif choice == "4":
            inventory_menu(player)
        elif choice == "5":
            save_game(player)
        elif choice == "6":
            slow_print("Goodbye, hero!")
            break
        else:
            print("❌ Invalid choice.")
            input("Press ENTER to continue...")


def new_game():
    name = input("Enter your hero name: ")
    player = Player(name)
    print(f"Welcome, {player.name}! Your journey begins...")
    return player


def main():
    clear_screen()
    print(Color.MAGENTA + "=" * 40)
    slow_print("     🗡️  RPG ADVENTURE  🛡️", 0.05, Color.CYAN)
    print(Color.MAGENTA + "=" * 40)
    slow_print("         Game by Azmii", 0.04, Color.YELLOW)
    print(Color.MAGENTA + "-" * 40)

    loading_bar("Loading world", 5, 0.25, Color.GREEN)
    slow_print("Welcome, hero!", 0.05, Color.CYAN)
    print(Color.MAGENTA + "-" * 40)

    choice = input(Color.WHITE + "1. New Game\n2. Load Game\n> " + Color.RESET)

    if choice == "1":
        player = new_game()

    elif choice == "2":
        player = load_game()
        if player is None:
            input("\n❌ Save file not found. Tekan ENTER untuk kembali ke menu...")
            return main()

    else:
        print("❌ Pilihan tidak valid!")
        input("\nTekan ENTER untuk kembali ke menu...")
        return main()

    main_menu(player)


if __name__ == "__main__":
    main()
