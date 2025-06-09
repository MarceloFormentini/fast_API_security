# API com FastAPI

Este projeto demonstra uma aplicação simples em FastAPI seguindo padrões **MVC**, **Clean Code** e princípios **SOLID**, com:

* Autenticação via JWT (endpoints de cadastro e login de usuário)
* CRUD básico de **Time** (código e nome)
* Banco SQLite gerado automaticamente
* Configurações via arquivo **.env**

---

## Índice

1. [Estrutura do Projeto](#estrutura-do-projeto)
2. [Dependências](#dependências)
3. [Configuração de Variáveis de Ambiente (.env)](#configuração-de-variáveis-de-ambiente-env)
4. [Geração do Banco SQLite](#geração-do-banco-sqlite)
5. [Instalação e Execução](#instalação-e-execução)
6. [Endpoints e Testes com Postman](#endpoints-e-testes-com-postman)
7. [Padrões Aplicados](#padrões-aplicados)
8. [Checklist de Boas Práticas](#checklist-de-boas-práticas)

---

## Estrutura do Projeto

```
app/
├── __init__.py
├── main.py           # Inicialização da aplicação
├── config.py         # Carrega .env e Settings
├── database.py       # Engine, SessionLocal, Base
├── models.py         # ORM: User, Team
├── schemas.py        # Pydantic: UserCreate, UserRead, TeamCreate, TeamRead, Token
├── repositories.py   # Interfaces (IUserRepository, ITeamRepository) e implementações
├── services.py       # Lógica de negócio (AuthService, TeamService)
└── controllers.py    # Rotas, injeção de dependências e criação de tabelas

.env                   # Variáveis de ambiente (SECRET_KEY, DB_URL, etc.)
requirements.txt       # Dependências do projeto
README.md              # Este arquivo de documentação
```

---

## Dependências

```bash
pip install -r requirements.txt
```

- `fastapi + uvicorn[standard]`: framework web e servidor ASGI
- `sqlalchemy`: ORM
- `pydantic`: validação de dados (já vem com FastAPI)
- `passlib[bcrypt]`: hash de senhas
- `pyjwt`: geração/verificação de JWT
- `python-dotenv` (opcional): carregar .env com configurações
- `alembic` (opcional): versionamento de esquema do banco
- `python-multipart`: parse de formulários multipart/form-data (usado pelo `OAuth2PasswordRequestForm`)

---

## Configuração de Variáveis de Ambiente (.env)

Crie um arquivo `.env` na raiz do projeto:

```ini
# .env
SECRET_KEY=uma_chave_supersecreta
ACCESS_TOKEN_EXPIRE_MINUTES=120
SQLALCHEMY_DATABASE_URL=sqlite:///./test.db
```

### Carregando no `config.py`

```python
from dotenv import load_dotenv
from pydantic import BaseSettings
import os

load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "changeme123")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    SQLALCHEMY_DATABASE_URL: str = os.getenv(
        "SQLALCHEMY_DATABASE_URL", "sqlite:///./test.db"
    )

settings = Settings()
```

---

## Geração do Banco SQLite

1. A URL `sqlite:///./test.db` indica ao SQLAlchemy usar SQLite e criar (ou abrir) o arquivo `test.db` no diretório raiz.
2. Em `database.py`, configura-se:

   ```python
   engine = create_engine(
       settings.SQLALCHEMY_DATABASE_URL,
       connect_args={"check_same_thread": False}
   )
   SessionLocal = sessionmaker(...)
   Base = declarative_base()
   ```
3. Na execução da aplicação (`controllers.py` ou `main.py`):

   ```python
   from .database import engine, Base
   from .models import User, Team
   Base.metadata.create_all(bind=engine)
   ```

   * Se `test.db` não existir, será criado.
   * As tabelas `users` e `teams` serão materializadas.

---

## Instalação e Execução

1. **Virtualenv**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate   # Windows
   ```
2. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```
3. **Execute o servidor**:

   ```bash
   uvicorn app.main:app --reload
   ```
4. **Acesse**:

   * Swagger UI: `http://127.0.0.1:8000/docs`
   * Redoc:        `http://127.0.0.1:8000/redoc`

---

## Endpoints e Testes com Postman

1. **Registro** (`POST /register`)

   * Body JSON:

     ```json
     { "username": "joao", "password": "senha123" }
     ```
   * Resposta: `{ "id": 1, "username": "joao" }`

2. **Login** (`POST /login`)

   * Form data x-www-form-urlencoded:

     ```text
     username=joao
     password=senha123
     ```
   * Resposta: `{ "access_token": "<JWT>", "token_type": "bearer" }`

3. **Criar Time** (`POST /teams`)

   * Header `Authorization: Bearer <JWT>`
   * Body JSON:

     ```json
     { "code": "FLA", "name": "Flamengo" }
     ```
   * Resposta: `{ "id": 1, "code": "FLA", "name": "Flamengo" }`

4. **Listar Times** (`GET /teams`)

   * Header `Authorization: Bearer <JWT>`
   * Resposta: `[{ "id": 1, "code": "FLA", "name": "Flamengo" }]`

> **Dica**: No Postman, armazene o token em uma *environment variable* e utilize `{{token}}` nos headers.

---

## Padrões Aplicados

* **MVC**:

  * *Model*: `models.py` (SQLAlchemy) + `schemas.py` (Pydantic)
  * *View/Controller*: `controllers.py` (rotas FastAPI)
  * *Service*: `services.py` (regras de negócio)
* **Clean Code**: nomes claros, responsabilidades isoladas, modularização
* **SOLID**:

  * Single Responsibility: cada classe faz uma coisa
  * Open/Closed: extensível sem modificações diretas
  * Liskov Substitution: repositórios seguem interfaces
  * Interface Segregation: separação de contratos
  * Dependency Inversion: serviços dependem de abstrações

---

## Checklist de Boas Práticas

* ✅ **HTTPS/HSTS** em produção
* ✅ **Cookies HttpOnly/Secure** (se usar cookies)
* ✅ **CORS** restrito
* ✅ **Rate Limiting** em endpoints sensíveis
* ✅ **Headers de Segurança** (CSP, X-Frame, X-Content-Type)
* ✅ **Logs e Monitoramento** de falhas de autenticação e CSRF

---