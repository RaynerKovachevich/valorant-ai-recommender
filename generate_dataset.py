import pandas as pd
import random

NUM_PLAYERS = 5000

roles = ["duelist", "initiator", "controller", "sentinel"]
maps = ["Ascent", "Bind", "Lotus", "Split", "Icebox", "Sunset"]
playstyles = ["aggressive", "balanced", "passive"]

agents = {
    "duelist": ["Jett", "Phoenix", "Reyna", "Raze", "Neon", "Yoru", "Iso"],
    "initiator": ["Sova", "Breach", "Skye", "KAY/O", "Fade", "Gekko"],
    "controller": ["Viper", "Omen", "Brimstone", "Astra", "Harbor", "Clove"],
    "sentinel": ["Sage", "Cypher", "Killjoy", "Chamber", "Deadlock", "Vyse"]
}

aim_types = ["precise", "spray", "burst", "hybrid"]

# More varied eDPI ranges per playstyle AND role
edpi_ranges = {
    "aggressive": {
        "duelist": (300, 400),
        "initiator": (280, 360),
        "controller": (260, 340),
        "sentinel": (240, 320)
    },
    "balanced": {
        "duelist": (260, 340),
        "initiator": (240, 320),
        "controller": (220, 300),
        "sentinel": (200, 280)
    },
    "passive": {
        "duelist": (240, 320),
        "initiator": (220, 300),
        "controller": (200, 280),
        "sentinel": (180, 260)
    }
}

# Agent preferences based on multiple factors
agent_weights = {
    "aggressive": {
        "duelist": 0.6,    # 60% chance for aggressive players
        "initiator": 0.2,
        "controller": 0.1,
        "sentinel": 0.1
    },
    "balanced": {
        "duelist": 0.25,
        "initiator": 0.35,
        "controller": 0.25,
        "sentinel": 0.15
    },
    "passive": {
        "duelist": 0.15,
        "initiator": 0.2,
        "controller": 0.3,
        "sentinel": 0.35
    }
}

def weighted_role_choice(playstyle, aggressiveness):
    """Choose role based on playstyle and aggressiveness with some randomness"""
    weights = agent_weights[playstyle].copy()
    
    # Add randomness based on aggressiveness level
    if aggressiveness >= 7:
        weights["duelist"] += 0.1
        weights["sentinel"] -= 0.1
    elif aggressiveness <= 3:
        weights["sentinel"] += 0.1
        weights["duelist"] -= 0.1
    
    # Normalize weights
    total = sum(weights.values())
    weights = {k: v/total for k, v in weights.items()}
    
    return random.choices(list(weights.keys()), weights=list(weights.values()))[0]

def assign_agent(role, ability_usage):
    """Assign agent with some variation based on ability usage"""
    available_agents = agents[role].copy()
    
    # Some agents are more popular for high ability usage
    if ability_usage >= 7 and role == "initiator":
        # Prefer utility-heavy initiators
        if "Sova" in available_agents and random.random() < 0.3:
            return "Sova"
        if "Fade" in available_agents and random.random() < 0.25:
            return "Fade"
    
    if ability_usage <= 3 and role == "duelist":
        # Prefer aim-focused duelists
        if "Reyna" in available_agents and random.random() < 0.25:
            return "Reyna"
        if "Jett" in available_agents and random.random() < 0.25:
            return "Jett"
    
    return random.choice(available_agents)

def generate_row():
    playstyle = random.choice(playstyles)
    aggressiveness = random.randint(1, 10)
    ability_usage = random.randint(1, 10)
    
    # Choose role based on playstyle and aggressiveness
    role = weighted_role_choice(playstyle, aggressiveness)
    
    # Assign agent based on role and ability usage
    agent = assign_agent(role, ability_usage)
    
    # Get eDPI range based on playstyle AND role
    edpi_min, edpi_max = edpi_ranges[playstyle][role]
    
    # Add some variation based on aim type
    aim_type = random.choice(aim_types)
    if aim_type == "precise":
        edpi_min = max(180, edpi_min - 40)  # Lower sens for precise aim
    elif aim_type == "spray":
        edpi_max = min(450, edpi_max + 40)  # Higher sens for spray
    
    edpi = random.randint(edpi_min, edpi_max)

    sens_800 = round(edpi / 800, 3)
    sens_1600 = round(edpi / 1600, 3)
    
    favorite_map = random.choice(maps)
    hours_played = random.randint(10, 1500)
    
    # Make winrates more correlated with role preference
    base_winrate = random.uniform(35, 65)
    winrate_duelist = round(base_winrate + (10 if role == "duelist" else random.uniform(-10, 5)), 2)
    winrate_initiator = round(base_winrate + (10 if role == "initiator" else random.uniform(-10, 5)), 2)
    winrate_controller = round(base_winrate + (10 if role == "controller" else random.uniform(-10, 5)), 2)
    winrate_sentinel = round(base_winrate + (10 if role == "sentinel" else random.uniform(-10, 5)), 2)
    
    # Clamp winrates to realistic values
    winrate_duelist = max(20, min(80, winrate_duelist))
    winrate_initiator = max(20, min(80, winrate_initiator))
    winrate_controller = max(20, min(80, winrate_controller))
    winrate_sentinel = max(20, min(80, winrate_sentinel))
    
    return {
        "playstyle": playstyle,
        "preferred_role": role,
        "favorite_map": favorite_map,
        "recommended_agent": agent,
        "edpi": edpi,
        "dpi_800": 800,
        "sens_800": sens_800,
        "dpi_1600": 1600,
        "sens_1600": sens_1600,
        "aim_type": aim_type,
        "ability_usage": ability_usage,
        "aggressiveness": aggressiveness,
        "hours_played": hours_played,
        "winrate_duelist": winrate_duelist,
        "winrate_initiator": winrate_initiator,
        "winrate_controller": winrate_controller,
        "winrate_sentinel": winrate_sentinel,
    }

dataset = [generate_row() for _ in range(NUM_PLAYERS)]
df = pd.DataFrame(dataset)
df.to_csv("valorant_dataset.csv", index=False)
print(f"Dataset successfully generated: valorant_dataset.csv with {NUM_PLAYERS} rows")

# Show agent distribution for verification
print("\n[Dataset Statistics]")
print(f"Agent distribution:")
print(df["recommended_agent"].value_counts())
print(f"\nRole distribution:")
print(df["preferred_role"].value_counts())
