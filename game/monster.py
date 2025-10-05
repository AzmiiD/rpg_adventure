import random

class Monster:
    def __init__(self, player_level):
        names = ["Slime", "Goblin", "Wolf", "Zombie", "Skeleton"]
        self.name = random.choice(names)
        self.level = random.randint(player_level, player_level + 2)
        self.hp = random.randint(50, 80) + self.level * 5
        self.attack_power = random.randint(6, 10) + self.level * 2
        self.exp_reward = self.level * 20
        self.gold_reward = random.randint(10, 30)

    def attack(self):
        return random.randint(self.attack_power - 3, self.attack_power + 3)
