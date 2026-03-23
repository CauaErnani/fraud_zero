from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Cliente
from app.schemas import (
    ClientePublico,
    Token,
)
from app.security import (
    create_access_token,
    get_current_user,
    verify_password,
)

router = APIRouter(prefix='/auth', tags=['auth'])
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
T_Session = Annotated[AsyncSession, Depends(get_session)]
T_CurrentUser = Annotated[Cliente, Depends(get_current_user)]


@router.post('/login', response_model=Token)
async def login_for_access_token(
    form_data: T_OAuth2Form,
    session: T_Session,
):
    """
    Faz login usando o **CNPJ** no campo 'username'
    e a **API Key** no campo 'password'.
    """

    cliente = await session.scalar(
        select(Cliente).where(Cliente.cnpj == form_data.username)
    )

    if not cliente:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='CNPJ ou senha incorretos',
        )

    if not verify_password(form_data.password, cliente.api_key_hash):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='CNPJ ou senha incorretos',
        )

    access_token = create_access_token(data={'sub': cliente.cnpj})

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/me', response_model=ClientePublico)
async def read_users_me(current_user: T_CurrentUser):
    return current_user
