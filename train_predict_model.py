import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

# -----------------------------
# 1. Load dataset
# -----------------------------
df = pd.read_csv("valorant_dataset.csv")

# Features and targets
categorical_cols = ["playstyle", "preferred_role", "favorite_map", "aim_type"]
numeric_cols = ["edpi", "ability_usage", "aggressiveness", "hours_played"]

X = df[categorical_cols + numeric_cols]
y_agent = df["recommended_agent"]
y_sens = df["sens_800"]  # Using sens_800 as reference sensitivity

# -----------------------------
# 2. Encode categorical features
# -----------------------------
encoder = OneHotEncoder(sparse_output=False)
X_encoded = encoder.fit_transform(X[categorical_cols])

X_final = np.hstack([X_encoded, X[numeric_cols].values])

# -----------------------------
# 3. Split dataset
# -----------------------------
X_train, X_test, y_agent_train, y_agent_test, y_sens_train, y_sens_test = train_test_split(
    X_final, y_agent, y_sens, test_size=0.2, random_state=42
)

# -----------------------------
# 4. Train models
# -----------------------------
# Agent prediction
agent_model = RandomForestClassifier(n_estimators=100, random_state=42)
agent_model.fit(X_train, y_agent_train)
accuracy = agent_model.score(X_test, y_agent_test)
print(f"[Model Training] Agent prediction accuracy: {accuracy:.2%}")

# Sensitivity prediction
sens_model = RandomForestRegressor(n_estimators=100, random_state=42)
sens_model.fit(X_train, y_sens_train)
r2_score = sens_model.score(X_test, y_sens_test)
print(f"[Model Training] Sensitivity prediction R²: {r2_score:.4f}")

# -----------------------------
# 5. Prediction function
# -----------------------------
def predict_agent_sens(input_dict):
    """
    input_dict = {
        "playstyle": "aggressive",
        "preferred_role": "duelist",
        "favorite_map": "Ascent",
        "aim_type": "precise",
        "edpi": 320,
        "ability_usage": 5,
        "aggressiveness": 7,
        "hours_played": 200
    }
    """
    # Encode categorical features
    input_df = pd.DataFrame([{
        "playstyle": input_dict["playstyle"],
        "preferred_role": input_dict["preferred_role"],
        "favorite_map": input_dict["favorite_map"],
        "aim_type": input_dict["aim_type"]
    }])

    X_input_cat = encoder.transform(input_df)

    # Numeric features
    X_input_num = np.array([[input_dict["edpi"],
                             input_dict["ability_usage"], input_dict["aggressiveness"],
                             input_dict["hours_played"]]])

    X_input_final = np.hstack([X_input_cat, X_input_num])

    # Predict agent and sensitivity
    recommended_agent = agent_model.predict(X_input_final)[0]
    recommended_sens = sens_model.predict(X_input_final)[0]

    return recommended_agent, round(recommended_sens, 3)

# -----------------------------
# 6. Usage example
# -----------------------------
if __name__ == "__main__":
    # Test with multiple profiles
    test_profiles = [
        {
            "name": "Aggressive Duelist",
            "playstyle": "aggressive",
            "preferred_role": "duelist",
            "favorite_map": "Ascent",
            "aim_type": "precise",
            "edpi": 320,
            "ability_usage": 3,
            "aggressiveness": 9,
            "hours_played": 500
        },
        {
            "name": "Passive Sentinel",
            "playstyle": "passive",
            "preferred_role": "sentinel",
            "favorite_map": "Bind",
            "aim_type": "spray",
            "edpi": 220,
            "ability_usage": 8,
            "aggressiveness": 2,
            "hours_played": 800
        },
        {
            "name": "Balanced Initiator",
            "playstyle": "balanced",
            "preferred_role": "initiator",
            "favorite_map": "Lotus",
            "aim_type": "burst",
            "edpi": 280,
            "ability_usage": 7,
            "aggressiveness": 5,
            "hours_played": 350
        }
    ]
    
    print("\n" + "="*60)
    print("TESTING PREDICTIONS")
    print("="*60)
    
    for profile in test_profiles:
        name = profile.pop("name")
        edpi = profile["edpi"]
        agent, sens_800 = predict_agent_sens(profile)
        sens_1600 = round(sens_800 / 2, 3)
        
        print(f"\n[{name}]")
        print(f"  Profile: {profile['playstyle']}, {profile['preferred_role']}, {profile['aim_type']}")
        print(f"  eDPI: {edpi}")
        print(f"  Recommended agent: {agent}")
        print(f"  Recommended sens @ 800 DPI: {sens_800}")
        print(f"  Recommended sens @ 1600 DPI: {sens_1600}")
    
    print("\n" + "="*60)
