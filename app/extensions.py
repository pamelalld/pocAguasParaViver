from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo

db = SQLAlchemy()

FUSO_BRASIL = ZoneInfo("America/Sao_Paulo")

def data_atual():
    return datetime.now(FUSO_BRASIL)