import os
from datetime import datetime, date, timezone, timedelta

class Settings:
    def carregar_env(self):
        pass
    def get_config(self, key):
        return os.getenv(key)

# Timezone do Brasil (UTC-3)
BRASILIA_TZ = timezone(timedelta(hours=-3))

def hoje_brasilia() -> date:
    """
    Retorna a data atual no horário de Brasília
    """
    return datetime.now(BRASILIA_TZ).date()

def agora_brasilia() -> datetime:
    """
    Retorna a data/hora atual no horário de Brasília
    """
    return datetime.now(BRASILIA_TZ)
