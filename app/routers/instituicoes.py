import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Cliente
from app.schemas import ClienteCreateResponse, ClienteSchema
from app.security import get_password_hash

router = APIRouter(prefix='/instituicoes', tags=['instituicoes'])


@router.post('/', response_model=ClienteCreateResponse, status_code=201)
async def create_instituicao(
    instituicao: ClienteSchema,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    query_nome = select(Cliente).where(
        Cliente.nome_instituicao == instituicao.nome_instituicao
    )
    result_nome = await session.execute(query_nome)
    if result_nome.scalar_one_or_none():
        raise HTTPException(
            status_code=400, detail='Nome da instituição já cadastrado.'
        )

    query = select(Cliente).where(Cliente.cnpj == instituicao.cnpj)
    result = await session.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail='CNPJ já cadastrado.')

    plain_api_key = f'fz_{secrets.token_urlsafe(32)}'

    hashed_key = get_password_hash(plain_api_key)

    new_client = Cliente(
        nome_instituicao=instituicao.nome_instituicao,
        cnpj=instituicao.cnpj,
        api_key_hash=hashed_key,
    )

    session.add(new_client)
    await session.commit()
    await session.refresh(new_client)

    return {
        'id': new_client.id,
        'nome_instituicao': new_client.nome_instituicao,
        'cnpj': new_client.cnpj,
        'ativo': new_client.ativo,
        'data_criacao': new_client.data_criacao,
        'ultimo_acesso': new_client.ultimo_acesso,
        'api_key': plain_api_key,
    }
