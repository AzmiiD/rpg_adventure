# Simple quest definitions and factory functions

def make_kill_quest(qid, monster_name, count, gold_reward=50, exp_reward=40, items_reward=None):
    return {
        "id": qid,
        "desc": f"Defeat {count} {monster_name}(s)",
        "type": "kill",
        "target": monster_name,
        "target_count": count,
        "progress": 0,
        "reward": {"gold": gold_reward, "exp": exp_reward, "items": items_reward or []},
        "status": "in_progress"
    }

# some sample quests
SAMPLE_QUESTS = [
    make_kill_quest("q1", "Goblin", 3, gold_reward=80, exp_reward=120),
    make_kill_quest("q2", "Slime", 5, gold_reward=40, exp_reward=60)
]
