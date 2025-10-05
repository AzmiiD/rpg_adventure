import json
import os

SAVE_FILE = "save.json"

def save_game(player):
    data = {
        "name": player.name,
        "hp": player.hp,
        "max_hp": player.max_hp,
        "attack": player.attack,
        "defense": player.defense,
        "inventory": player.inventory,
        "equipment": player.equipment,
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("💾 Game tersimpan!")

def load_game():
    if not os.path.exists(SAVE_FILE):
        print("❌ Tidak ada data save ditemukan! Silakan mulai game baru dulu.")
        return None

    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        from .player import Player
        player = Player(data["name"])
        player.hp = data["hp"]
        player.max_hp = data["max_hp"]
        player.attack = data["attack"]
        player.defense = data["defense"]
        player.inventory = data.get("inventory", [])
        player.equipment = data.get("equipment", {})
        print(f"✅ Save data {player.name} berhasil dimuat!")
        return player
    except (json.JSONDecodeError, KeyError):
        print("⚠️ File save rusak atau kosong! Mulai game baru aja.")
        return None
