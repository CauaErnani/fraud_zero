from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TransacaoEntrada(BaseModel):
    transaction_id: str
    user_id: str
    type: str
    amount: float
    oldbalanceOrig: float
    newbalanceOrig: float
    oldbalanceDest: float
    newbalanceDest: float


class PredicaoRisco(BaseModel):
    analysis_id: str
    is_fraud: bool
    risk_score: float


class LogAnalise(BaseModel):
    id_log: str
    timestamp: datetime
    dados_entrada: str
    predicao_retornada: str
    cliente_id: str


class ClienteBase(BaseModel):
    nome_instituicao: str
    cnpj: str = Field(..., min_length=14, max_length=14)


class ClientePublico(ClienteBase):
    id: str
    ativo: bool
    data_criacao: datetime
    ultimo_acesso: datetime | None = None
    model_config = ConfigDict(from_attributes=True)


class ClienteSchema(ClienteBase):
    pass


class ClienteCreateResponse(ClientePublico):
    api_key: str
