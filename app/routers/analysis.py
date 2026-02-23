from http import HTTPStatus

from fastapi import APIRouter

from app.schemas import TransacaoEntrada

router = APIRouter(prefix='/analysis', tags=['analysis'])


@router.post('/analisar/', status_code=HTTPStatus.CREATED)
def solicitar_analise(transacao: TransacaoEntrada):
    return transacao
