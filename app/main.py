from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, candidates, swipes, agent

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tinder IDO API",
    version="0.1.0",
    description="MVP matchmaking backend with Agent/Matchmaker placeholders",
)

app.include_router(auth.router)
app.include_router(candidates.router)
app.include_router(swipes.router)
app.include_router(agent.router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
