import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.v1.endpoinds.user import router as user
from app.core.config import settings
from starlette.middleware.sessions import SessionMiddleware
app = FastAPI()


app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


origins = [
    'http://localhost:3000',
    'http://127.0.0:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)


app.include_router(user, prefix='/api')


if __name__ == '__main__':
    uvicorn.run('main:app')