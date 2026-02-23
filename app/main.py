from fastapi import FastAPI

from app.routers import analysis

app = FastAPI(title='Vai corinthians!!')

app.include_router(analysis.router)


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}
