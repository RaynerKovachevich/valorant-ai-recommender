from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from API.schemas import PlayerInput, PredictionOutput
from API.predictor import predict_player

app = FastAPI(
    title="Valorant AI Recommender",
    description="Get personalized Valorant agent and sensitivity recommendations based on your playstyle",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", summary="API Status")
async def root():
    """Health check endpoint"""
    return {
        "message": "Valorant AI Recommender API is running!",
        "status": "online",
        "version": "1.0.0"
    }

@app.post("/predict", response_model=PredictionOutput, summary="Get agent and sensitivity prediction")
async def predict_endpoint(player: PlayerInput):
    """
    Endpoint to predict recommended agent with sensitivity for both 800 and 1600 DPI
    based on player profile and preferences.
    """
    try:
        # Convert PlayerInput to dict for predictor
        player_data = player.model_dump()
        
        result = predict_player(player_data)
        
        # Check for errors
        if "error" in result:
            raise HTTPException(status_code=503, detail=result["error"])
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)