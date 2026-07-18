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
        "r16": [{"p1": players[i], "p2": players[i+1], "s1_1": None, "s1_2": None, "s2_1": None, "s2_2": None, "w": 0} for i in range(0, 16, 2)],
        "qf": [{"p1": "TBD", "p2": "TBD", "s1_1": None, "s1_2": None, "s2_1": None, "s2_2": None, "w": 0} for _ in range(4)],
        "sf": [{"p1": "TBD", "p2": "TBD", "s1_1": None, "s1_2": None, "s2_1": None, "s2_2": None, "w": 0} for _ in range(2)],
        "f": [{"p1": "TBD", "p2": "TBD", "s1_1": None, "s1_2": None, "s2_1": None, "s2_2": None, "w": 0}],
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
            data = json.loads(json_str)
            
            # --- AUTOMATIC MIGRATION PIPELINE ---
            migrated = False
            for key in ["r16", "qf", "sf", "f"]:
                if key in data:
                    for match in data[key]:
                        if match.get('w') == 0:  
                            for score_field in ['s1_1', 's1_2', 's2_1', 's2_2']:
                                if match.get(score_field) == 0:
                                    match[score_field] = None
                                    migrated = True
            if migrated:
                with open(DATA_FILE, "w") as f_out:
                    f_out.write(f"window.tournamentData = {json.dumps(data, indent=4)};\ninitRender();")
            
            return data
    except:
        return None

def edit_player_names():
    data = load_data()
    if not data:
        print("❌ Data error. Initialize tournament first.")
        return
    
    print("\n--- Current Round of 16 Matchups ---")
    for idx, m in enumerate(data["r16"]):
        print(f"Match {idx+1}: (1) {m['p1']} vs (2) {m['p2']}")
        
    m_idx = int(input("\nSelect Match Number you want to edit: ")) - 1
    p_select = input("Edit Player 1 or Player 2? (Type 1 or 2): ")
    new_name = input("Enter new/corrected name: ").strip()
    
    if p_select == "1":
        data["r16"][m_idx]["p1"] = new_name
    elif p_select == "2":
        data["r16"][m_idx]["p2"] = new_name
        
    save_data(data)
    print("📝 Player name updated locally! Remember to run push.bat to update the website.")

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
    
    # Unique 1-Leg Logic Condition for the Grand Final
    if round_key == "f":
        match['s1_1'] = int(input(f"  {match['p1']} Goals: ") or 0)
        match['s1_2'] = None
        match['s2_1'] = int(input(f"  {match['p2']} Goals: ") or 0)
        match['s2_2'] = None
        
        tot1 = match['s1_1']
        tot2 = match['s2_1']
    else:
        # Standard 2-Leg Logic for prior rounds
        match['s1_1'] = int(input(f"  {match['p1']} (Leg 1 Goals): ") or 0)
        match['s1_2'] = int(input(f"  {match['p1']} (Leg 2 Goals): ") or 0)
        match['s2_1'] = int(input(f"  {match['p2']} (Leg 1 Goals): ") or 0)
        match['s2_2'] = int(input(f"  {match['p2']} (Leg 2 Goals): ") or 0)
        
        tot1 = match['s1_1'] + match['s1_2']
        tot2 = match['s2_1'] + match['s2_2']
    
    if tot1 > tot2: 
        match['w'] = 1
    elif tot2 > tot1: 
        match['w'] = 2
    else: 
        match['w'] = int(input("Draw! Who won penalties? (Type 1 or 2): "))

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
        print("3. Edit/Correct Player Names")
        print("4. Exit Terminal")
        c = input("Action: ")
        if c == "1": initialize_tournament()
        elif c == "2": update_scores()
        elif c == "3": edit_player_names()
        elif c == "4": break

if __name__ == "__main__":
    main()
