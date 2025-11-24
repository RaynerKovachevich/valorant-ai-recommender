import pandas as pd
import numpy as np
import random
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

# -----------------------------
# 1. Load dataset
# -----------------------------
df = pd.read_csv("valorant_dataset.csv")

# Features and Targets
X = df[["playstyle", "preferred_role", "favorite_map", "weapon_preference", "combat_distance", "dpi", "edpi"]]
y_agent = df["recommended_agent"]
y_sens = df["sens"]

# -----------------------------
# 2. Convert categorical to numbers
# -----------------------------
categorical_cols = ["playstyle", "preferred_role", "favorite_map", "weapon_preference", "combat_distance"]
encoder = OneHotEncoder(sparse_output=False)
X_encoded = encoder.fit_transform(X[categorical_cols])

X_final = np.hstack([X_encoded, X[["dpi", "edpi"]].values])

# -----------------------------
# 3. Split dataset
# -----------------------------
X_train, X_test, y_agent_train, y_agent_test, y_sens_train, y_sens_test = train_test_split(
    X_final, y_agent, y_sens, test_size=0.2, random_state=42
)

# -----------------------------
# 4. Train models
# -----------------------------
# RandomForestClassifier for Agent
agent_model = RandomForestClassifier(n_estimators=100, random_state=42)
agent_model.fit(X_train, y_agent_train)
print("Agent prediction accuracy:", agent_model.score(X_test, y_agent_test))

# RandomForestRegressor for sensitivity
sens_model = RandomForestRegressor(n_estimators=100, random_state=42)
sens_model.fit(X_train, y_sens_train)
print("Sens prediction  R^2:", sens_model.score(X_test, y_sens_test))

# -----------------------------
# 5. Prediction function for user
# -----------------------------
def predict_agent_sens(input_dict):
    """
    input_dict = {
    "playstyle": "aggresive",
    "preferred_role": "duelist",
    "favorite_map": "Ascent",
    "weapon_preference": "rifles",
    "combat_distance": "mid-range",
    "dpi": 800,
    "edpi": 320

    }
    """

# Create DataFrame so encoder sees valid feature names
    input_df = pd.DataFrame([{
        "playstyle": input_dict["playstyle"],
        "preferred_role": input_dict["preferred_role"],
        "favorite_map": input_dict["favorite_map"],
        "weapon_preference": input_dict["weapon_preference"],
        "combat_distance": input_dict["combat_distance"]
    }])

    X_input_cat = encoder.transform(input_df)
    X_input_final = np.hstack([X_input_cat, [[input_dict["dpi"], input_dict["edpi"]]]])

# Predictions
    recommended_agent = agent_model.predict(X_input_final)[0]
    recommended_sens = sens_model.predict(X_input_final)[0]

    return recommended_agent, round(recommended_sens, 3)

# -----------------------------
# 6. Usage example
# -----------------------------
if __name__ == "__main__":
    example_input = {
        "playstyle": "aggressive",
        "preferred_role": "duelist",
        "favorite_map": "Abyss",
        "weapon_preference": "rifles",
        "combat_distance": "mid-range",
        "dpi": 800,
        "edpi": 320
    }
    agent, sens = predict_agent_sens(example_input)
    print("Recommended agent:", agent)
    print("Recommended sens:", sens)
