# MindHub Backend

Backend da plataforma MindHub - Sistema de agendamento de consultas psicológicas.

## � Pré-requisitos

### 1. Instalar uv (Gerenciador de Pacotes Python)

**uv** é um gerenciador de pacotes Python extremamente rápido, escrito em Rust.

#### Linux/macOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows (PowerShell):

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Documentação oficial**: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

### 2. Instalar Docker

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/macOS/Linux)
- Ou Docker Engine para Linux: [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)

## �🚀 Início Rápido

### Passo a Passo Completo

#### 1. Clone o repositório

```bash
git clone https://github.com/gabriellivalelia/mindhub-backend
cd mindhub-backend
```

#### 2. Instalar dependências

```bash
uv sync
```

#### 3. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` se necessário (os valores padrão já funcionam para desenvolvimento local).

#### 4. Iniciar o banco de dados

```bash
docker compose up -d
```

Isso iniciará:

- MongoDB na porta 27017
- Redis na porta 6379

#### 5. Popular o banco de dados (Seeds)

```bash
uv run poe seed
```

Este comando irá criar:

- 12 especialidades psicológicas
- 10 abordagens terapêuticas
- 27 estados e ~5.570 municípios (todos do Brasil, via API IBGE)
- 8 psicólogos com disponibilidades para as próximas 2 semanas

**Nota**: A primeira execução pode levar alguns minutos para buscar todos os municípios do IBGE.

**Credenciais dos psicólogos criados**: Senha `Senha@123`

Veja [Seeds README](src/infra/database/seeds/README.md) para mais detalhes.

#### 6. Iniciar o servidor

```bash
uv run poe dev
```

O servidor estará disponível em: `http://localhost:8000`

Documentação da API: `http://localhost:8000/docs`

## 📝 Comandos Disponíveis

```bash
uv run poe dev          # Inicia o servidor de desenvolvimento
```

## 🗄️ Banco de Dados

### Requisitos

- MongoDB 7.0+
- Redis 7.0+

### Conexão

Configure as variáveis de ambiente no arquivo `.env`:

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=mindhub
REDIS_URL=redis://localhost:6379
```

## 📚 Documentação

- [Seeds README](src/infra/database/seeds/README.md) - Sistema de seeds
- [Diagramas UML](docs/uml/) - Arquitetura do sistema
- [Relatório](docs/project_report)

## 📖 Links Úteis

- **Documentação do uv**: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)
- **Documentação do FastAPI**: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **API do IBGE** (usada nos seeds): [https://servicodados.ibge.gov.br/api/docs/localidades](https://servicodados.ibge.gov.br/api/docs/localidades)
