# CRM de Leads

Aplicação simples construída com FastAPI para gerenciar leads manuais e recebidos via webhook. O CRM mantém um funil com cinco etapas:

1. novo lead
2. qualificação
3. triagem
4. proposta negociação
5. fechado / perdido

## Pré-requisitos

- Python 3.11+
- Pipenv ou pip

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows PowerShell
pip install -r requirements.txt
```

## Executando o servidor

```bash
uvicorn main:app --reload
```

Acesse `http://127.0.0.1:8000/` para visualizar a página principal do CRM com o
funil e a listagem de leads. A documentação interativa continua disponível em
`http://127.0.0.1:8000/docs`.

## Endpoints principais

- `GET /stages` – Lista as etapas do funil.
- `POST /leads` – Cria um lead manualmente.
- `POST /webhook/leads` – Recebe um lead via webhook.
- `GET /leads` – Lista todos os leads.
- `GET /leads/{id}` – Busca detalhes de um lead específico.
- `PATCH /leads/{id}/stage` – Atualiza a etapa do funil de um lead.

## Webhook de exemplo

```bash
curl -X POST http://127.0.0.1:8000/webhook/leads \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Maria Souza",
        "email": "maria@example.com",
        "phone": "+55 11 99999-0000",
        "company": "Empresa Exemplo",
        "stage": "qualificação"
      }'
```

## Testando rapidamente

```bash
python -m compileall .
```
