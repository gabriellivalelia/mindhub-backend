# Sistema de Seeds do MindHub

Este diretório contém o sistema de seeds para popular o banco de dados MongoDB com dados iniciais do projeto MindHub.

## 🚀 Como Executar

### Opção 1: Usando poethepoet (Recomendado)

```bash
cd mindhub-backend
uv run poe seed
```

### Opção 2: Executando diretamente com Python

```bash
cd mindhub-backend
uv run python src/infra/database/seeds/run_seeds.py
```

## 📊 O que será criado

O sistema de seeds irá popular o banco de dados com:

### 1. **12 Especialidades Psicológicas**

- Ansiedade
- Depressão
- Relacionamentos
- Autoestima
- Transtornos Alimentares
- Luto
- Estresse
- TOC
- TDAH
- Orientação Vocacional
- Trauma
- Sexualidade

### 2. **10 Abordagens Terapêuticas**

- Terapia Cognitivo-Comportamental (TCC)
- Psicanálise
- Psicodrama
- Gestalt-Terapia
- Terapia Sistêmica
- ACT (Terapia de Aceitação e Compromisso)
- Análise Comportamental
- Humanista
- Junguiana
- EMDR

### 3. **Dados Geográficos (IBGE)** 🇧🇷

- **27 estados brasileiros**
- **~5.570 municípios** (todos os municípios do Brasil)

Os dados geográficos são obtidos **automaticamente** da API oficial do IBGE:

- API: https://servicodados.ibge.gov.br/api/v1/localidades
- Dados sempre atualizados com a fonte oficial
- Inclui todos os estados e municípios do Brasil
- Não requer manutenção manual dos dados

Estados incluídos (todos):

- Todos os 26 estados + Distrito Federal
- Exemplos: MG, SP, RJ, BA, PR, RS, PE, CE, PA, AM, etc.

### 4. **8 Psicólogos**

Cada psicólogo inclui:

- Dados pessoais completos
- 2-3 especialidades
- 1-2 abordagens terapêuticas
- Público-alvo (crianças, adolescentes, adultos, idosos, casais)
- **Disponibilidades dinâmicas**: ~70-80 horários para as próximas 2 semanas
  - Horários: 8h às 18h (exceto 12h-13h)
  - Apenas dias úteis (segunda a sexta)
  - Intervalos de 1 hora

**Credenciais de acesso (todos os psicólogos):**

- Senha: `Senha@123`

**Psicólogos criados:**

1. Ana Paula Silva (BH) - ana.silva@mindhub.com
2. Carlos Eduardo Santos (BH) - carlos.santos@mindhub.com
3. Mariana Costa (Contagem) - mariana.costa@mindhub.com
4. Roberto Oliveira (Uberlândia) - roberto.oliveira@mindhub.com
5. Juliana Ferreira (Juiz de Fora) - juliana.ferreira@mindhub.com
6. Fernando Alves (São Paulo) - fernando.alves@mindhub.com
7. Patricia Lima (BH) - patricia.lima@mindhub.com
8. André Rodrigues (Betim) - andre.rodrigues@mindhub.com

## 🔄 Comportamento dos Seeds

### População Automática

Os seeds verificam **automaticamente** se o banco de dados está vazio antes de popular:

#### Dados Geográficos (IBGE)

- **Fonte**: API oficial do IBGE (atualizada automaticamente)
- **Detecção**: Se não houver estados no banco, busca todos os 27 estados e ~5.570 municípios
- **Processo**:
  1. Busca estados da API do IBGE
  2. Busca municípios de cada estado (em paralelo, limitado a 5 requisições simultâneas)
  3. Salva no MongoDB apenas se não existirem
- **Vantagens**:
  - Dados sempre atualizados com a fonte oficial
  - Sem necessidade de manutenção manual
  - Cobertura completa do território brasileiro

**Nota**: A primeira execução pode levar alguns minutos devido ao volume de dados (~5.570 municípios).

### Idempotência

Os seeds são **idempotentes**, ou seja, podem ser executados múltiplas vezes sem duplicar dados:

- ✅ Se um registro já existe (mesmo nome/email), ele é pulado
- ✅ Novos registros são adicionados normalmente
- ✅ Seguro executar após atualizações do código

### Disponibilidades Dinâmicas

As disponibilidades dos psicólogos são geradas **dinamicamente** baseadas na data de execução:

- **Início**: Dia seguinte à execução do seed
- **Duração**: 14 dias (2 semanas)
- **Horários**: 8h, 9h, 10h, 11h, 14h, 15h, 16h, 17h, 18h
- **Dias**: Apenas dias úteis (exclui fins de semana)

**Exemplo:**
Se você executar o seed em 1º de novembro de 2025 (sexta-feira), as disponibilidades serão criadas de:

- 4 de novembro de 2025 (segunda) até
- 15 de novembro de 2025 (sexta)

### Re-execução

Para atualizar as disponibilidades com novas datas:

1. **Opção 1**: Delete os psicólogos existentes e execute novamente
2. **Opção 2**: Execute diretamente no MongoDB:
   ```javascript
   db.users.deleteMany({ crp: { $exists: true } });
   ```
3. Execute o seed novamente: `uv run poe seed`

## ⚙️ Requisitos

- MongoDB rodando (via Docker ou local)
- Redis rodando (via Docker ou local)
- Conexão com a internet (para buscar dados do IBGE)
- Variáveis de ambiente configuradas (`.env`)
- Dependências instaladas: `uv sync`

## 🐛 Troubleshooting

### Erro: "Connection refused"

**Problema**: MongoDB não está rodando.

**Solução**:

```bash
cd mindhub-backend
docker compose up -d
```

### Erro: "Duplicate key error"

**Problema**: Tentando criar registro que já existe.

**Solução**: Os seeds já pulam registros duplicados automaticamente. Se persistir, limpe a coleção específica.

### Disponibilidades não aparecem

**Problema**: Pode ser timezone ou seed antigo.

**Solução**: Delete os psicólogos e execute novamente:

```bash
# No mongo shell
db.users.deleteMany({ crp: { $exists: true } })
```

### Erro ao buscar dados do IBGE

**Problema**: API do IBGE não está acessível ou conexão com internet instável.

**Solução**:

1. Verifique sua conexão com a internet
2. Tente novamente (a API do IBGE pode estar temporariamente indisponível)
3. Os dados já salvos não serão afetados (o seed pula registros existentes)

## 📝 Adicionando Novos Seeds

Para adicionar novos dados:

1. **Edite os arquivos em `data/`**: Adicione novos registros aos arrays
2. **Ou crie novo seeder**: Siga o padrão dos existentes
3. **Atualize `run_seeds.py`**: Adicione a chamada ao novo seeder

## 🎯 Ordem de Execução

Os seeds são executados nesta ordem (importante por causa das dependências):

1. ✅ Especialidades (independente)
2. ✅ Abordagens (independente)
3. ✅ Geografia - Estados (independente)
4. ✅ Geografia - Cidades (depende de Estados)
5. ✅ Psicólogos (depende de Especialidades, Abordagens e Cidades)

## 🧪 Testando

Após executar os seeds, você pode verificar se tudo foi criado:

```javascript
// No mongo shell
use mindhub

// Contar registros
db.specialties.countDocuments()  // Deve retornar 12
db.approaches.countDocuments()   // Deve retornar 10
db.states.countDocuments()       // Deve retornar 27 (todos os estados)
db.cities.countDocuments()       // Deve retornar ~5570 (todos os municípios)
db.users.countDocuments({ crp: { $exists: true } })  // Deve retornar 8

// Ver um psicólogo com disponibilidades
db.users.findOne({ crp: { $exists: true } })

// Ver alguns estados e cidades
db.states.find().limit(5)
db.cities.find({ "state.abbreviation": "MG" }).limit(10)
```

## 📚 Referências

- [Beanie ODM](https://beanie-odm.dev/)
- [Motor (MongoDB Async Driver)](https://motor.readthedocs.io/)
- [MongoDB](https://www.mongodb.com/docs/)
