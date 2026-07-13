import json
import random
import os

DATA_FILE = "data.js"

def initialize_tournament():
    print("\n=== Initialize Season 13 Fixtures ===")
    players = []
    for i in range(1, 17):
        name = input(f"Enter Name for Player {i} (or click Enter for 'Player {i}'): ").strip()
        players.append(name if name else f"Player {i}")
    
    random.shuffle(players)
    
    data = {
        "r16": [{"p1": players[i], "p2": players[i+1], "s1_1": 0, "s1_2": 0, "s2_1": 0, "s2_2": 0, "w": 0} for i in range(0, 16, 2)],
        "qf": [{"p1": "TBD", "p2": "TBD", "s1_1": 0, "s1_2": 0, "s2_1": 0, "s2_2": 0, "w": 0} for _ in range(4)],
        "sf": [{"p1": "TBD", "p2": "TBD", "s1_1": 0, "s1_2": 0, "s2_1": 0, "s2_2": 0, "w": 0} for _ in range(2)],
        "f": [{"p1": "TBD", "p2": "TBD", "s1_1": 0, "s1_2": 0, "s2_1": 0, "s2_2": 0, "w": 0}],
        "champion": "TBD"
    }
    save_data(data)
    print("\n✅ New 16-Player Bracket Generated Layout! Ready to play.")

def save_data(data):
    with open(DATA_FILE, "w") as f:
        f.write(f"window.tournamentData = {json.dumps(data, indent=4)};\ninitRender();")

def load_data():
    if not os.path.exists(DATA_FILE):
        return None
    try:
        with open(DATA_FILE, "r") as f:
            content = f.read()
            json_str = content.split("window.tournamentData = ")[1].split(";\ninitRender();")[0]
            return json.loads(json_str)
    except:
        return None

def update_scores():
    data = load_data()
    if not data:
        print("❌ Data error. Initialize tournament first.")
        return

    print("\n--- Update Scores ---")
    print("1. Round of 16")
    print("2. Quarter Finals")
    print("3. Semi Finals")
    print("4. Grand Final Match")
    round_choice = input("Choose Round: ")
    
    if round_choice == "1": round_key = "r16"
    elif round_choice == "2": round_key = "qf"
    elif round_choice == "3": round_key = "sf"
    elif round_choice == "4": round_key = "f"
    else: return

    for idx, m in enumerate(data[round_key]):
        print(f"Match {idx+1}: {m['p1']} vs {m['p2']}")
    
    m_idx = int(input("Select Match Number: ")) - 1
    match = data[round_key][m_idx]
    
    print(f"\nEntering scores for: {match['p1']} vs {match['p2']}")
    match['s1_1'] = int(input(f"  {match['p1']} (Leg 1 Goals): ") or 0)
    match['s1_2'] = int(input(f"  {match['p1']} (Leg 2 Goals): ") or 0)
    match['s2_1'] = int(input(f"  {match['p2']} (Leg 1 Goals): ") or 0)
    match['s2_2'] = int(input(f"  {match['p2']} (Leg 2 Goals): ") or 0)
    
    tot1 = match['s1_1'] + match['s1_2']
    tot2 = match['s2_1'] + match['s2_2']
    
    if tot1 > tot2: match['w'] = 1
    elif tot2 > tot1: match['w'] = 2
    else: match['w'] = int(input("Draw on aggregate! Who won penalties? (1 or 2): "))

    winner_name = match['p1'] if match['w'] == 1 else match['p2']

    # Dynamic Auto-Advance Pipeline
    if round_key == "r16":
        qf_idx = m_idx // 2
        if m_idx % 2 == 0: data['qf'][qf_idx]['p1'] = winner_name
        else: data['qf'][qf_idx]['p2'] = winner_name
    elif round_key == "qf":
        sf_idx = m_idx // 2
        if m_idx % 2 == 0: data['sf'][sf_idx]['p1'] = winner_name
        else: data['sf'][sf_idx]['p2'] = winner_name
    elif round_key == "sf":
        if m_idx == 0: data['f'][0]['p1'] = winner_name
        else: data['f'][0]['p2'] = winner_name
    elif round_key == "f":
        data['champion'] = winner_name

    save_data(data)
    print("\n🏆 Score Registered and advanced successfully!")

def main():
    while True:
        print("\n=== eFootball S13 Dashboard ===")
        print("1. Initialize New Tournament Layout")
        print("2. Enter Live Match Scores")
        print("3. Exit Terminal")
        c = input("Action: ")
        if c == "1": initialize_tournament()
        elif c == "2": update_scores()
        elif c == "3": break

if __name__ == "__main__":
    main()
