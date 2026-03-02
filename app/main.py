from fastapi import FastAPI

from app.routers import analysis, instituicoes

app = FastAPI(title='Vai corinthians!!')

app.include_router(instituicoes.router)
app.include_router(analysis.router)


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}
