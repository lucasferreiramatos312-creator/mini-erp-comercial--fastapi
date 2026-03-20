from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import produtos,auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(produtos.router)
app.include_router(auth.router)