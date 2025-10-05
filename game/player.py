import random
from game.items import ITEMS
from game.equipment import EQUIPMENTS

class Player:
    def __init__(self, name, hp=100, max_hp=100, gold=50, level=1, exp=0, inventory=None,
                 equipped=None, quests=None):
        self.name = name
        self.max_hp = max_hp
        self.hp = hp
        self.gold = gold
        self.level = level
        self.exp = exp
        self.inventory = inventory or []       # list of item dicts
        # equipped: {"weapon": item_dict or None, "armor": item_dict or None}
        self.equipped = equipped or {"weapon": None, "armor": None}
        self.quests = quests or []             # list of quest dicts
        self.defending = False                 # flag for defend action

    # --- Combat / stats ---
    def base_attack(self):
        return random.randint(8, 14) + (self.level * 2)

    def attack(self, attack_type="normal"):
        """
        attack_type: "normal", "heavy"
        heavy: higher damage but chance to miss
        """
        weapon_bonus = 0
        if self.equipped.get("weapon"):
            weapon_bonus = self.equipped["weapon"].get("damage", 0)

        if attack_type == "normal":
            base = self.base_attack()
            return base + weapon_bonus
        elif attack_type == "heavy":
            # 60% hit chance
            if random.random() < 0.6:
                return int((self.base_attack() + weapon_bonus) * 1.8)
            else:
                return 0  # miss
        else:
            return self.base_attack() + weapon_bonus

    def defense_value(self):
        armor_bonus = 0
        if self.equipped.get("armor"):
            armor_bonus = self.equipped["armor"].get("defense", 0)
        return armor_bonus

    def take_damage(self, dmg):
        if self.defending:
            dmg = max(0, dmg - int(self.defense_value() * 1.5))
        else:
            dmg = max(0, dmg - self.defense_value())
        self.hp -= dmg
        return dmg

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    # --- XP & Level ---
    def gain_exp(self, amount):
        self.exp += amount
        needed = self.level * 50
        while self.exp >= needed:
            self.exp -= needed
            self.level_up()
            needed = self.level * 50

    def level_up(self):
        self.level += 1
        self.max_hp += 10
        self.hp = self.max_hp
        print(f"\n🎉 {self.name} leveled up to Level {self.level}!")

    # --- Inventory & equipment ---
    def add_item(self, item):
        self.inventory.append(item)

    def use_item(self, item_index):
        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            if item["type"] == "heal":
                self.heal(item["effect"])
                print(f"💊 You used {item['name']} and healed {item['effect']} HP!")
                self.inventory.pop(item_index)
            else:
                print("Item can't be used directly.")
        else:
            print("Invalid item index.")

    def equip_from_inventory(self, inv_index):
        """Equip an equipment item from inventory by index (moves it to equipped)."""
        if 0 <= inv_index < len(self.inventory):
            item = self.inventory[inv_index]
            if item.get("slot") not in ("weapon", "armor"):
                print("This item is not equippable.")
                return
            slot = item["slot"]
            # unequip current to inventory
            if self.equipped.get(slot):
                self.inventory.append(self.equipped[slot])
            self.equipped[slot] = item
            self.inventory.pop(inv_index)
            print(f"✅ Equipped {item['name']} to {slot}.")
        else:
            print("Invalid inventory index.")

    def unequip(self, slot):
        if slot in self.equipped and self.equipped[slot]:
            self.inventory.append(self.equipped[slot])
            print(f"⚪ Unequipped {self.equipped[slot]['name']} from {slot}.")
            self.equipped[slot] = None
        else:
            print("Nothing to unequip in that slot.")

    # --- Quests ---
    def add_quest(self, quest_dict):
        # quest_dict: from quest module (id, desc, type, target, progress, reward)
        self.quests.append(quest_dict)
        print(f"📜 New quest accepted: {quest_dict['desc']}")

    def update_quests_on_kill(self, monster):
        changed = False
        for q in self.quests:
            if q["status"] != "in_progress":
                continue
            if q["type"] == "kill" and monster.name == q["target"]:
                q["progress"] += 1
                print(f"📈 Quest progress: {q['desc']} ({q['progress']}/{q['target_count']})")
                if q["progress"] >= q["target_count"]:
                    q["status"] = "completed"
                    print(f"🎉 Quest completed: {q['desc']}")
                    # reward
                    r = q.get("reward", {})
                    self.gold += r.get("gold", 0)
                    self.gain_exp(r.get("exp", 0))
                    for it in r.get("items", []):
                        self.add_item(it)
                    changed = True
        return changed
