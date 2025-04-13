from fastapi import FastAPI
from app.router import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Universal Code Analyzer", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
app.include_router(router)




