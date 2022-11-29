"""Project {{name_project}}
    """


from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.auth.exceptions import AuthJWTException, authjwt_ex
from app.auth.router import router as auth

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth)
app.add_exception_handler(AuthJWTException, authjwt_ex)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", host="127.0.0.1",
        port=5050, reload=True,
    )
