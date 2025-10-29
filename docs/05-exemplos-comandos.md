
# Exemplos e Comandos

## Instalação de dependências

```bash
pip install -r requirements.txt
```

## Execução local

```bash
uvicorn src.main:app --reload
```

## Rodar lint

```bash
flake8 src/
```

## Rodar testes

```bash
# Testes unitários
pytest tests/

# Testes específicos
pytest tests/test_arquivo.py -v

# Testes end-to-end (e2e) - interface web
python run_e2e_tests.py

# Ou executar manualmente (servidor deve estar rodando):
pytest tests/test_login_e2e.py -v --browser chromium --headed=false
```
