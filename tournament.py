import json
import random
import os

DATA_FILE = "data.js"

def initialize_tournament():
    print("--- Initialize Season 13 Fixtures ---")
    players = []
    for i in range(1, 17):
        name = input(f"Enter Name for Player {i} (or press Enter for 'Player {i}'): ").strip()
        players.append(name if name else f"Player {i}")
    
    random.shuffle(players)
    
    data = {
        "r16": [{"p1": players[i], "p2": players[i+1], "s1_1": 0, "s1_2": 0, "s2_1": 0, "s2_2": 0, "w": 0} for i in range(0, 16, 2)],
        "qf": [{"p1": "TBD", "p2": "TBD", "s1_1": 0, "s1_2": 0, "s2_1": 0, "s2_2": 0, "w": 0} for _ in range(4)],
        "champion": "TBD"
    }
    save_data(data)
    print("\n✅ Match fixtures generated randomly across Left and Right sides!")

def save_data(data):
    with open(DATA_FILE, "w") as f:
        f.write(f"const tournamentData = {json.dumps(data, indent=4)};")

def load_data():
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, "r") as f:
        content = f.read()
        json_str = content.replace("const tournamentData = ", "").rstrip(";")
        return json.loads(json_str)

def update_scores():
    data = load_data()
    if not data:
        print("❌ No tournament initialized yet. Choose Option 1 first.")
        return

    print("\n--- Update Scores ---")
    print("1. Round of 16")
    print("2. Quarter Finals")
    round_choice = input("Select round: ")
    
    round_key = "r16" if round_choice == "1" else "qf"
    
    for idx, m in enumerate(data[round_key]):
        print(f"Match {idx+1}: {m['p1']} vs {m['p2']}")
    
    m_idx = int(input("Select Match Number: ")) - 1
    match = data[round_key][m_idx]
    
    print(f"\nEntering scores for: {match['p1']} vs {match['p2']}")
    match['s1_1'] = int(input(f"{match['p1']} Leg 1 Goals: ") or 0)
    match['s1_2'] = int(input(f"{match['p1']} Leg 2 Goals: ") or 0)
    match['s2_1'] = int(input(f"{match['p2']} Leg 1 Goals: ") or 0)
    match['s2_2'] = int(input(f"{match['p2']} Leg 2 Goals: ") or 0)
    
    tot1 = match['s1_1'] + match['s1_2']
    tot2 = match['s2_1'] + match['s2_2']
    
    if tot1 > tot2:
        match['w'] = 1
        print(f"🎉 Winner: {match['p1']}")
    elif tot2 > tot1:
        match['w'] = 2
        print(f"🎉 Winner: {match['p2']}")
    else:
        match['w'] = int(input("Aggregate Draw! Who won the Penalty Shootout? (1 for Player 1, 2 for Player 2): "))

    # Auto-advance logic to Quarter Finals
    if round_key == "r16":
        qf_idx = m_idx // 2
        winner_name = match['p1'] if match['w'] == 1 else match['p2']
        if m_idx % 2 == 0:
            data['qf'][qf_idx]['p1'] = winner_name
        else:
            data['qf'][qf_idx]['p2'] = winner_name

    save_data(data)
    print("🏆 Data written to data.js successfully!")

def main():
    while True:
        print("\n=== eFootball S13 CMD Tournament Dashboard ===")
        print("1. Initialize New Tournament (Randomize & Edit Names)")
        print("2. Update Live Scores & Auto-Advance")
        print("3. Exit")
        choice = input("Enter option (1-3): ")
        if choice == "1": initialize_tournament()
        elif choice == "2": update_scores()
        elif choice == "3": break

if __name__ == "__main__":
    main()
