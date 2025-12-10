from pydantic import BaseModel, Field
from typing import Literal, Annotated

# Match the exact values from generate_dataset.py
Playstyle = Literal['aggressive', 'balanced', 'passive']
Role = Literal['duelist', 'initiator', 'controller', 'sentinel']
MapName = Literal['Ascent', 'Bind', 'Haven', 'Split', 'Icebox', 'Breeze', 'Fracture', 'Pearl', 'Lotus', 'Sunset', 'Abyss']
AimType = Literal['precise', 'spray', 'burst', 'hybrid']

class PlayerInput(BaseModel):
    """Player profile input for predictions"""
    playstyle: Playstyle = Field(..., description="Player's playstyle")
    preferred_role: Role = Field(..., description="Preferred agent role")
    favorite_map: MapName = Field(..., description="Favorite map")
    aim_type: AimType = Field(..., description="Aim style preference")
    edpi: Annotated[int, Field(ge=150, le=500, description="Effective DPI (DPI x Sensitivity)")]
    ability_usage: Annotated[int, Field(ge=1, le=10, description="Ability usage frequency (1=low, 10=high)")]
    aggressiveness: Annotated[int, Field(ge=1, le=10, description="Aggressiveness level (1=passive, 10=aggressive)")]
    hours_played: Annotated[int, Field(ge=0, le=10000, description="Total hours played")]
    
    class Config:
        json_schema_extra = {
            "example": {
                "playstyle": "aggressive",
                "preferred_role": "duelist",
                "favorite_map": "Ascent",
                "aim_type": "precise",
                "edpi": 320,
                "ability_usage": 5,
                "aggressiveness": 7,
                "hours_played": 200
            }
        }

class PredictionOutput(BaseModel):
    """Agent and sensitivity prediction output"""
    recommended_agent: str = Field(..., description="Recommended Valorant agent")
    recommended_sens_800: float = Field(..., description="Recommended sensitivity at 800 DPI")
    recommended_sens_1600: float = Field(..., description="Recommended sensitivity at 1600 DPI")
    edpi: int = Field(..., description="Effective DPI (same for both DPI settings)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "recommended_agent": "Reyna",
                "recommended_sens_800": 0.4,
                "recommended_sens_1600": 0.2,
                "edpi": 320
            }
        }    