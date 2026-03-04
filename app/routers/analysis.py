from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Cliente, LogAnalise
from app.schemas import PredicaoRisco, TransacaoEntrada
from app.security import get_current_user

router = APIRouter(prefix='/analysis', tags=['analysis'])
T_Session = Annotated[AsyncSession, Depends(get_session)]
T_CurrentUser = Annotated[Cliente, Depends(get_current_user)]

FRAUD_THRESHOLD_LIMIT = 8000
HIGH_RISK_SCORE = 0.95
LOW_RISK_SCORE = 0.05


@router.post(
    '/analisar/', status_code=HTTPStatus.CREATED, response_model=PredicaoRisco
)
async def solicitar_analise(
    session: T_Session, transacao: TransacaoEntrada, cliente: T_CurrentUser
):
    # 1. Lógica de predição provisória de teste(XGBoost)
    is_fraud = transacao.amount > FRAUD_THRESHOLD_LIMIT
    risk_score = HIGH_RISK_SCORE if is_fraud else LOW_RISK_SCORE

    db_log = LogAnalise(
        dados_entrada=transacao.model_dump_json(),
        predicao_retornada=f'is_fraud: {is_fraud}, score: {risk_score}',
        cliente_id=cliente.id,
    )

    session.add(db_log)
    await session.commit()
    await session.refresh(db_log)

    return {
        'analysis_id': db_log.id_log,
        'is_fraud': is_fraud,
        'risk_score': risk_score,
    }
