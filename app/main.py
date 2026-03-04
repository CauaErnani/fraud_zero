from fastapi import FastAPI

from app.routers import analysis, auth, instituicoes

app = FastAPI(title='Vai corinthians!!')

app.include_router(instituicoes.router)
app.include_router(analysis.router)
app.include_router(auth.router)


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}
