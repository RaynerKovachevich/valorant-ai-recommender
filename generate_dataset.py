import pandas as pd
import random

# Number of players to generate
NUM_PLAYERS = 500

# Full list of 2025 Valorant agents
agents = [
    "Astra", "Breach", "Brimstone", "Chamber", "Clove", "Cypher", "Deadlock",
    "Fade", "Gekko", "Harbor", "Iso", "Jett", "KAY/O", "Killjoy", "Neon",
    "Omen", "Phoenix", "Raze", "Reyna", "Sage", "Skye", "Sova", "Tejo",
    "Veto", "Viper", "Vyse", "Waylay", "Yoru"
]

# Features
playstyles = ["aggressive", "passive", "balanced", "utility-focused", "op-player"]
roles = ["duelist", "controller", "initiator", "sentinel"]
maps = ["Abyss", "Ascent", "Bind", "Corrode", "Haven", "Pearl", "Split", "Lotus", "Sunset"]
weapons = ["rifles", "snipers", "smgs", "shotguns"]
distances = ["close-range", "mid-range", "long-range"]
dpis = [800, 1600]  # Standard DPI options

# eDPI ranges per role (beginner-friendly)
edpi_ranges = {
    "duelist": (300, 380),
    "initiator": (280, 360),
    "controller": (250, 330),
    "sentinel": (220, 300)
}

# Function to assign an agent based on role and playstyle
def assign_agent(role, playstyle):
    role_mapping = {
        "duelist": ["Jett", "Reyna", "Raze", "Neon", "Yoru", "Iso", "Waylay", "Phoenix"],
        "initiator": ["Sova", "Breach", "Skye", "KAY/O", "Fade", "Gekko", "Tejo"],
        "controller": ["Brimstone", "Omen", "Viper", "Astra", "Harbor", "Clove"],
        "sentinel": ["Sage", "Cypher", "Killjoy", "Chamber", "Deadlock", "Vyse", "Veto"]
    }

    # Filter agents by playstyle
    if playstyle == "aggressive":
        # Aggressive players: prefer duelists and initiators that are combat-focused
        if role in ["duelist", "initiator"]:
            candidates = role_mapping[role]
        else:
            candidates = role_mapping[role]
    elif playstyle == "passive":
        # Passive players: prefer sentinel or controller style agents
        if role in ["controller", "sentinel"]:
            candidates = role_mapping[role]
        else:
            candidates = role_mapping[role]
    else:
        # Balanced / utility-focused / op-player: cualquier agente del rol
        candidates = role_mapping[role]

    return random.choice(candidates)

# Generate synthetic player data
data = []
for _ in range(NUM_PLAYERS):
    playstyle = random.choice(playstyles)
    role = random.choice(roles)
    favorite_map = random.choice(maps)
    weapon = random.choice(weapons)
    distance = random.choice(distances)
    agent = assign_agent(role, playstyle)  

    # Choose DPI
    dpi = random.choice(dpis)

    # Assign eDPI within role range
    edpi_min, edpi_max = edpi_ranges[role]
    edpi = random.randint(edpi_min, edpi_max)

    # Calculate sensitivity
    sens = round(edpi / dpi, 3)

    data.append([
        sens, dpi, edpi, playstyle, role, favorite_map, weapon, distance, agent
    ])

# Create DataFrame
columns = [
    "sens", "dpi", "edpi",
    "playstyle", "preferred_role", "favorite_map",
    "weapon_preference", "combat_distance", "recommended_agent"
]

df = pd.DataFrame(data, columns=columns)

# Save the dataset to CSV
df.to_csv("valorant_dataset.csv", index=False)
print("Dataset generated: valorant_dataset.csv with 500 rows")
