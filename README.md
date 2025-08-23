# Status Page: Datadog Monitor

Uma aplicação web simples e minimalista construída com **FastAPI** que exibe o status de serviços monitorados pelo **Datadog**.

A página consome os dados diretamente dos **monitores do Datadog**, exibindo seu estado atual em uma interface responsiva e elegante.

---

## Funcionalidades

- Exibe status de serviços (OK, ALERT, WARN, etc)
- Layout moderno e minimalista (HTML + CSS)
- Totalmente configurável via JSON
- Integração com Datadog via API
- Configuração por variáveis de ambiente
- Suporte a Docker

---

## Como usar

### 1. Clone o repositório

```bash
git clone https://github.com/rmnobarra/status-page-datadog-monitor.git
cd status-page-datadog-monitor
```

### 2. Configure o arquivo .env

Crie um .env com suas chaves do Datadog:

```bash
DATADOG_API_KEY=your_api_key
DATADOG_APP_KEY=your_app_key
DATADOG_API_URL=https://api.us5.datadoghq.com
```

### 3. Configure os monitores

Edite o arquivo monitors.json com os IDs e descrições dos monitores que deseja exibir:

```json
[
  {
    "url_monitor": "12345678",
    "nome_monitor": "API Principal",
    "descricao_monitor": "Verifica a saúde da API"
  },
  {
    "url_monitor": "87654321",
    "nome_monitor": "Banco de Dados",
    "descricao_monitor": "Monitoramento da instância RDS"
  }
]
```

### 4. Rodando com Docker

Build da imagem:

```bash
docker build -t status-page-app .
```

Execute o container:
```bash
docker run -p 8000:8000 --env-file .env status-page-app
```

Acesse:
```bash
http://localhost:8000
```

### Interface

Veja um exemplo da interface da aplicação:

![Status Page Screenshot](assets/screenshot.png)
