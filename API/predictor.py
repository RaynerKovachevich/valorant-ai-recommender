from pathlib import Path
import joblib
import pandas as pd
import numpy as np

# Models should be in backend/models/, not backend/API/models/
MODELS_DIR = Path(__file__).parent.parent / "models"

CLASSIFIER_FILE = MODELS_DIR / "agent_model.pkl"
REGRESSOR_FILE = MODELS_DIR / "sens_model.pkl"
ENCODER_FILE = MODELS_DIR / "encoder.pkl"

try:
    classifier = joblib.load(CLASSIFIER_FILE)
    regressor = joblib.load(REGRESSOR_FILE)
    encoder = joblib.load(ENCODER_FILE)
    print("[Predictor] Models loaded successfully")
except FileNotFoundError as e:
    print(f"[Predictor] Error loading models: {e}")
    classifier = None
    regressor = None
    encoder = None

# Categorical and numeric features (same as train_predict_model.py)
CATEGORICAL_COLS = ["playstyle", "preferred_role", "favorite_map", "aim_type"]
NUMERIC_COLS = ["edpi", "ability_usage", "aggressiveness", "hours_played"]

def predict_player(data: dict) -> dict:
    """
    Predict agent and sensitivity for a player
    
    Args:
        data: Dictionary with player features:
            - playstyle: "aggressive" | "balanced" | "passive"
            - preferred_role: "duelist" | "initiator" | "controller" | "sentinel"
            - favorite_map: str
            - aim_type: "precise" | "spray" | "burst" | "hybrid"
            - edpi: int
            - ability_usage: int (1-10)
            - aggressiveness: int (1-10)
            - hours_played: int
    
    Returns:
        Dictionary with:
            - recommended_agent: str
            - recommended_sens: float
    """
    if classifier is None or regressor is None or encoder is None:
        return {
            "recommended_agent": "MODEL_NOT_TRAINED",
            "recommended_sens": 0.0,
            "error": "Models not loaded. Please train the model first."
        }
    
    try:
        # Prepare categorical features
        cat_df = pd.DataFrame([{
            "playstyle": data["playstyle"],
            "preferred_role": data["preferred_role"],
            "favorite_map": data["favorite_map"],
            "aim_type": data["aim_type"]
        }])
        
        # Encode categorical features
        X_cat = encoder.transform(cat_df)
        
        # Prepare numeric features
        X_num = np.array([[
            data["edpi"],
            data["ability_usage"],
            data["aggressiveness"],
            data["hours_played"]
        ]])
        
        # Combine features
        X_final = np.hstack([X_cat, X_num])
        
        # Make predictions
        agent_pred = classifier.predict(X_final)[0]
        sens_800_pred = regressor.predict(X_final)[0]
        
        # Calculate sensitivity for both 800 and 1600 DPI
        sens_800 = round(float(sens_800_pred), 3)
        sens_1600 = round(sens_800 / 2, 3)  # 1600 DPI is half the sens of 800 DPI for same eDPI
        edpi = round(sens_800 * 800)
        
        return {
            "recommended_agent": agent_pred,
            "recommended_sens_800": sens_800,
            "recommended_sens_1600": sens_1600,
            "edpi": edpi
        }
    
    except Exception as e:
        return {
            "recommended_agent": "ERROR",
            "recommended_sens_800": 0.0,
            "recommended_sens_1600": 0.0,
            "edpi": 0,
            "error": str(e)
        }