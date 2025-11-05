# 📚 Books API - Tech Challenge Fase 1

> **Pós-Graduação em Machine Learning Engineering - FIAP**  
> Sistema de API RESTful para Consulta e Análise de Livros

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Objetivos](#-objetivos)
- [Arquitetura](#-arquitetura)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Documentação da API](#-documentação-da-api)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Deploy](#-deploy)
- [Vídeo de Apresentação](#-vídeo-de-apresentação)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Contribuidores](#-contribuidores)

---

## 🎯 Sobre o Projeto

Este projeto foi desenvolvido como parte do **Tech Challenge da Fase 1** do curso de Pós-Graduação em Machine Learning Engineering da FIAP. O desafio consiste em criar uma infraestrutura completa de dados, desde a extração até a disponibilização via API pública, pensada para ser consumida por cientistas de dados e sistemas de recomendação.

### O Problema

Uma empresa de recomendação de livros está em sua fase inicial e não possui uma base de dados estruturada. Como Engenheiro(a) de Machine Learning, o desafio é:

1. **Extrair** dados de uma fonte web (web scraping)
2. **Transformar** e estruturar os dados
3. **Disponibilizar** via API RESTful pública
4. **Documentar** e preparar para consumo ML

### A Solução

Desenvolvemos um pipeline completo que:

- 🔍 **Extrai** dados de livros do site [books.toscrape.com](https://books.toscrape.com/)
- 📊 **Armazena** em formato estruturado (CSV)
- 🚀 **Disponibiliza** via API RESTful com 12 endpoints
- 🔐 **Protege** com autenticação JWT
- 📝 **Documenta** automaticamente com Swagger UI
- ☁️ **Deploya** em produção com disponibilidade

---

## 🎓 Objetivos

### Objetivos Principais

- ✅ Criar sistema de web scraping robusto e automatizado
- ✅ Implementar API RESTful completa e funcional
- ✅ Estabelecer autenticação e segurança (JWT)
- ✅ Documentar API com Swagger/OpenAPI
- ✅ Realizar deploy em ambiente de produção
- ✅ Preparar dados para consumo de modelos ML

---

## 🏗️ Arquitetura

### Visão Geral do Pipeline

```url: https://drive.google.com/file/d/1DWrHJBm1BlOA1uJHs8izMSYgwhBQvopi/view?usp=sharing```

### Componentes Principais

1. **Módulo de Scraping** (`scripts/`)
   - Extração automatizada de dados
   - Tratamento de paginação
   - Validação de dados

2. **API RESTful** (`src/`)
   - Flask Framework
   - Autenticação JWT
   - Documentação Swagger
   - Tratamento de erros

3. **Armazenamento** (`data/`)
   - Formato CSV estruturado
   - Pandas para manipulação
   - Otimizado para ML

4. **Deploy** (Produção)
   - Servidor web configurado (CPanel)
   - HTTPS ativo

---

## 🛠️ Tecnologias Utilizadas

### Backend & API
- **Python** - Linguagem principal
- **Flask** - Framework web
- **Flasgger** - Documentação Swagger automática
- **PyJWT** - Autenticação JWT

### Data Processing
- **Pandas** - Manipulação de dados
- **BeautifulSoup4** - Web scraping
- **Requests** - HTTP requests

### Deploy & DevOps
- **CPanel** - Servidor web
- **SSL/TLS** - Segurança HTTPS

### Documentação
- **Swagger UI** - Interface interativa da API

---

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)
- Git
- Ambiente virtual (recomendado)

### Passo 1: Clone o Repositório

```bash
git clone https://github.com/jgmsgabriel/bookapi-ml-engineering-postech-desafio.git
cd bookapi-ml-engineering-postech-desafio
```

### Passo 2: Crie e Ative o Ambiente Virtual

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Passo 3: Instale as Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# JWT Configuration
JWT_SECRET=seu_secret_key_aqui_mude_em_producao
JWT_ALGORITHM=HS256
JWT_EXP_DELTA_SECONDS=3600

# API Configuration
BOOKS_CSV_PATH=./data/dados-books.csv

# Authentication (altere em produção!)
TEST_USERNAME=admin
TEST_PASSWORD=secret

# Swagger
SWAGGER_TITLE=Catálogo API Scrape Books
```

### Passo 6: Inicie a API

```bash
# Modo desenvolvimento
python -m src.main

```

A API estará disponível em:
- **Local**: http://localhost:5000
- **Swagger UI**: http://localhost:5000/docs/

---

## 📖 Documentação da API

### URL Base

- **Produção**: https://dunstudio.com.br
- **Local**: http://localhost:5000

### Swagger UI

Acesse a documentação interativa completa em:
- **Produção**: https://dunstudio.com.br/docs/
- **Local**: http://localhost:5000/docs/

### Autenticação

A API utiliza **JWT (JSON Web Token)** para autenticação. Para acessar endpoints protegidos:

1. Faça login em `/api/v1/auth/login`
2. Copie o token retornado
3. No Swagger UI, clique em "Authorize"
4. Cole: `Bearer SEU_TOKEN_AQUI`
5. Agora você pode acessar endpoints protegidos

### Endpoints Disponíveis

#### 🔐 Autenticação

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| POST | `/api/v1/auth/login` | Realiza login e retorna token JWT | Não |
| POST | `/api/v1/auth/refresh` | Renova token JWT expirado | Sim |

#### 📚 Livros

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| GET | `/api/v1/books` | Lista todos os livros | Sim |
| GET | `/api/v1/books/{id}` | Detalhes de um livro específico | Sim |
| GET | `/api/v1/books/search` | Busca por título e/ou categoria | Sim |
| GET | `/api/v1/books/top-rated` | Livros com melhor avaliação | Sim |
| GET | `/api/v1/books/price-range` | Filtra por faixa de preço | Sim |
| GET | `/api/v1/scrape-book/{id}` | Enriquece dados com scraping | Sim |

#### 🏷️ Categorias

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| GET | `/api/v1/categories` | Lista todas as categorias | Sim |

#### 📊 Estatísticas

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| GET | `/api/v1/stats/overview` | Estatísticas gerais | Sim |
| GET | `/api/v1/stats/categories` | Estatísticas por categoria | Sim |

#### 🏥 Health Check

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| GET | `/api/v1/health` | Verifica status da API | Não |

---

## 💡 Exemplos de Uso

### 1. Fazer Login

**Request:**
```bash
curl -X POST "https://dunstudio.com.br/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "secret"
  }'
```

**Response (200 OK):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNzYyMzA0ODAwfQ.signature"
}
```

### 2. Listar Todos os Livros

**Request:**
```bash
curl -X GET "https://dunstudio.com.br/api/v1/books" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**Response (200 OK):**
```json
[
  {
    "title": "A Light in the Attic",
    "price": 51.77,
    "rating": 3,
    "availability": "In stock",
    "category": "Poetry",
    "image_url": "https://books.toscrape.com/media/cache/...",
    "detail_url": "https://books.toscrape.com/catalogue/..."
  },
  {
    "title": "Tipping the Velvet",
    "price": 53.74,
    "rating": 1,
    "availability": "In stock",
    "category": "Historical Fiction",
    "image_url": "https://books.toscrape.com/media/cache/...",
    "detail_url": "https://books.toscrape.com/catalogue/..."
  }
]
```

### 3. Buscar Livros por Título

**Request:**
```bash
curl -X GET "https://dunstudio.com.br/api/v1/books/search?title=Light" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**Response (200 OK):**
```json
[
  {
    "title": "A Light in the Attic",
    "price": 51.77,
    "rating": 3,
    "availability": "In stock",
    "category": "Poetry"
  }
]
```

### 4. Obter Detalhes de um Livro

**Request:**
```bash
curl -X GET "https://dunstudio.com.br/api/v1/books/0" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**Response (200 OK):**
```json
{
  "title": "A Light in the Attic",
  "price": 51.77,
  "rating": 3,
  "availability": "In stock",
  "category": "Poetry",
  "image_url": "https://books.toscrape.com/media/cache/...",
  "detail_url": "https://books.toscrape.com/catalogue/..."
}
```

### 5. Listar Categorias

**Request:**
```bash
curl -X GET "https://dunstudio.com.br/api/v1/categories" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**Response (200 OK):**
```json
[
  "Add a comment",
  "Adult Fiction",
  "Art",
  "Biography",
  "Business",
  "Childrens",
  "Classics",
  "Contemporary",
  "Fantasy",
  "Fiction",
  "Historical Fiction",
  "History",
  "Horror",
  "Mystery",
  "Philosophy",
  "Poetry",
  "Psychology",
  "Romance",
  "Science Fiction",
  "Sequential Art",
  "Spirituality",
  "Sports and Games",
  "Suspense",
  "Thriller",
  "Travel",
  "Young Adult"
]
```

### 6. Estatísticas Gerais

**Request:**
```bash
curl -X GET "https://dunstudio.com.br/api/v1/stats/overview" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**Response (200 OK):**
```json
{
  "total_books": 1000,
  "average_price": 35.85,
  "rating_distribution": {
    "1": 204,
    "2": 202,
    "3": 193,
    "4": 203,
    "5": 198
  }
}
```

### 7. Filtrar por Faixa de Preço

**Request:**
```bash
curl -X GET "https://dunstudio.com.br/api/v1/books/price-range?min=10&max=20" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**Response (200 OK):**
```json
[
  {
    "title": "Sharp Objects",
    "price": 13.99,
    "rating": 4,
    "category": "Mystery"
  },
  {
    "title": "The Requiem Red",
    "price": 19.89,
    "rating": 5,
    "category": "Historical Fiction"
  }
]
```

### 8. Livros com Melhor Avaliação

**Request:**
```bash
curl -X GET "https://dunstudio.com.br/api/v1/books/top-rated" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**Response (200 OK):**
```json
[
  {
    "title": "The Requiem Red",
    "price": 19.89,
    "rating": 5,
    "category": "Historical Fiction"
  },
  {
    "title": "Starving Hearts",
    "price": 55.29,
    "rating": 5,
    "category": "Contemporary"
  }
]
```

### 9. Enriquecimento com Scraping

**Request:**
```bash
curl -X GET "https://dunstudio.com.br/api/v1/scrape-book/0" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**Response (200 OK):**
```json
{
  "title": "A Light in the Attic",
  "price": 51.77,
  "rating": 3,
  "product_description": "It's hard to imagine a world without A Light in the Attic...",
  "number_of_reviews": "0"
}
```

### 10. Health Check

**Request:**
```bash
curl -X GET "https://dunstudio.com.br/api/v1/health:"
```

**Response (200 OK):**
```json
{
  "api_status": "ok",
  "data_status": "connected",
  "records": 1000
}
```

---

## 🔐 Segurança e Autenticação

### Como Funciona o JWT

1. **Login**: O usuário envia credenciais para `/api/v1/auth/login`
2. **Token**: A API retorna um token JWT válido por 1 hora
3. **Autorização**: O cliente envia o token no header `Authorization: Bearer {token}`
4. **Validação**: A API valida o token em cada requisição
5. **Renovação**: Token pode ser renovado em `/api/v1/auth/refresh`

### Configuração de Segurança

**⚠️ IMPORTANTE**: Em produção, sempre:

1. ✅ Altere `JWT_SECRET` para um valor forte e único
2. ✅ Altere credenciais de teste (`TEST_USERNAME` e `TEST_PASSWORD`)
3. ✅ Use HTTPS (nunca HTTP em produção)
4. ✅ Configure rate limiting
5. ✅ Monitore logs de acesso

---

## ☁️ Deploy

### Produção

A API está deployada e operacional em:

🔗 **URL Base**: https://dunstudio.com.br  
📝 **Swagger UI**: https://dunstudio.com.br/docs/

### Tecnologias de Deploy

- **Servidor**: CPanel
- **SSL**: Let's Encrypt
- **Domain**: dunstudio.com.br

---

## 🎬 Vídeo de Apresentação

> 📹 https://youtu.be/NU3RSvxfLIc

O vídeo inclui:
- ✅ Demonstração técnica do projeto
- ✅ Apresentação da arquitetura e pipeline
- ✅ Execução de chamadas reais à API em produção
- ✅ Comentários sobre boas práticas implementadas

---

## 📁 Estrutura do Projeto

```
bookapi-ml-engineering-postech-desafio/
│
├── src/                          # Código fonte da API
│   ├── __init__.py              # Inicialização do Flask app + Swagger
│   ├── main.py                  # Rotas e endpoints da API
│   ├── config.py                # Configurações e variáveis de ambiente
│   └── utilidades.py            # Funções auxiliares (JWT, scraping, CSV)
│
├── scripts/                      # Scripts de automação
│   └── scrape_books.py          # Web scraping automatizado
│
├── data/                         # Dados extraídos
│   └── dados-books.csv          # Base de dados em CSV
│
├── docs/                         # Documentação adicional
│   ├── arquitetura-draw.txt      # URL arquiteturas
│   ├── arquitetura1.png          # Arquitetura aplicação
│   ├── arquitetura2.png          # Arquitetura aplicação
│   └── fluxo-ml.png              # Arquitetura aplicação
│
├── .env                          # Exemplo de variáveis de ambiente
├── .gitignore                    # Arquivos ignorados pelo Git
├── requirements.txt              # Dependências Python
└── README.md                     # Este arquivo

```

### Módulos Principais

#### `src/__init__.py`
- Inicialização do Flask
- Configuração do Swagger UI
- Carregamento de configurações

#### `src/main.py`
- Definição de todas as rotas da API
- Lógica de negócio dos endpoints
- Tratamento de erros

#### `src/config.py`
- Variáveis de ambiente
- Configurações de JWT
- Paths e credenciais

#### `src/utilidades.py`
- Autenticação JWT
- Web scraping sob demanda
- Leitura e processamento de CSV

---

## 🎓 Conceitos de ML Aplicados

### Preparação de Dados para Machine Learning

Este projeto foi desenvolvido pensando em facilitar o consumo por modelos de ML:

1. **Features Estruturadas**
   - Dados em formato tabular (CSV)
   - Colunas bem definidas
   - Tipos de dados consistentes

2. **Endpoints ML-Ready**
   - `/api/v1/books` - Dataset completo
   - `/api/v1/stats/*` - Features agregadas
   - Filtros para segmentação de dados

3. **Possíveis Aplicações ML**
   - 🎯 Sistema de recomendação de livros
   - 💰 Predição de preços
   - ⭐ Classificação de ratings
   - 📊 Análise de sentimento (descrições)
   - 🏷️ Clustering de categorias

### Exemplo de Uso em ML

```python
import pandas as pd
import requests

# Obter token
auth_response = requests.post(
    "https://dunstudio.com.br/api/v1/auth/login",
    json={"username": "admin", "password": "secret"}
)
token = auth_response.json()["token"]

# Obter dados
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "https://dunstudio.com.br/api/v1/books",
    headers=headers
)

# Converter para DataFrame
df = pd.DataFrame(response.json())

# Pronto para ML!
print(df.head())
print(df.describe())

# Exemplo: Treinar modelo de predição de rating
from sklearn.ensemble import RandomForestClassifier

X = df[['price']]  # Features
y = df['rating']    # Target

model = RandomForestClassifier()
model.fit(X, y)
```

---

## 📈 Melhorias Futuras

### Próximos Passos

- [ ] Implementar cache Redis para performance
- [ ] Adicionar rate limiting por usuário
- [ ] Criar endpoints para CRUD completo
- [ ] Implementar versionamento da API (v2, v3...)
- [ ] Adicionar testes automatizados (pytest)
- [ ] Criar pipeline CI/CD
- [ ] Implementar logging estruturado
- [ ] Dashboard de monitoramento (Grafana)
- [ ] Websockets para updates em tempo real
- [ ] Dockerização do projeto

### Integrações ML Planejadas

- [ ] Endpoint para predictions (`/api/v1/ml/predict`)
- [ ] Export de features para treinamento
- [ ] Versionamento de datasets
- [ ] A/B testing de modelos

---

## 👥 Contribuidores

- **João Gabriel Matheus da Silva Gabriel** - [GitHub](https://github.com/jgmsgabriel)

---

## 🙏 Agradecimentos

- **FIAP** - Pós-Graduação em Machine Learning Engineering
- **Comunidade Python** - Ferramentas e bibliotecas incríveis
- **Colegas de turma** - Discussões e colaborações valiosas

---

## 📞 Contato

**João Gabriel Matheus da Silva Gabriel**

- GitHub: [@jgmsgabriel](https://github.com/jgmsgabriel)
- LinkedIn: (https://www.linkedin.com/in/jgmsgabriel/)
- Email: jgmsgabriel@gmail.com

---

## 🔗 Links Importantes

- 🌐 **API em Produção**: https://dunstudio.com.br
- 📝 **Swagger UI**: https://dunstudio.com.br/docs/
- 💻 **Repositório GitHub**: https://github.com/jgmsgabriel/bookapi-ml-engineering-postech-desafio
- 📹 **Vídeo de Apresentação**: https://youtu.be/NU3RSvxfLIc
- 🎓 **Curso**: Pós-Graduação ML Engineering - FIAP

---

<div align="center">

Desenvolvido para o Tech Challenge Fase 1 - FIAP 2025

</div>
