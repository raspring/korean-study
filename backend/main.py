import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from database import engine, Base
from routers import auth, progress, quiz

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Korean Study API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(progress.router, prefix="/api/progress", tags=["progress"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["quiz"])

FRONTEND = os.path.join(os.path.dirname(__file__), "..", "index.html")


@app.get("/")
async def serve_frontend():
    return FileResponse(FRONTEND)
