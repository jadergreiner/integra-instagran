import os

class Settings:
    def carregar_env(self):
        pass
    def get_config(self, key):
        return os.getenv(key)
