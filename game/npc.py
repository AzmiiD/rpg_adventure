from game.quest import SAMPLE_QUESTS

class NPC:
    def __init__(self, name, quests=None):
        self.name = name
        self.quests = quests or []

    def talk(self, player):
        print(f"\n🧑 {self.name}: Hello, {player.name}!")
        # Offer first available quest that player doesn't have
        for q in self.quests:
            # check if player already accepted or completed
            have = any(player_q["id"] == q["id"] for player_q in player.quests)
            if not have:
                print(f"📜 I have a quest: {q['desc']}")
                choice = input("Accept quest? (y/n) > ")
                if choice.lower().startswith("y"):
                    player.add_quest(q.copy())
                else:
                    print("Maybe next time.")
                return
        # If no new quests
        print("I have no quests for you at the moment. Thank you!")
