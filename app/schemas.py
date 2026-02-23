from datetime import datetime

from pydantic import BaseModel


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
    
class ClientePublico(ClienteBase):
    id: str
    ativo: bool
    data_criacao: datetime
    ultimo_acesso: datetime
    
class ClienteSchema(ClienteBase):
    nome_instituicao: str
    
class ClienteAPI(ClientePublico):
    api_key_hash: str