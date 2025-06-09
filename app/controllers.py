from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from .database import SessionLocal, Base, engine
from .models import User, Team
from .schemas import UserCreate, UserRead, Token, TeamCreate, TeamRead
from .repositories import UserRepository, TeamRepository
from .services import AuthService, TeamService
import jwt
from .config import settings

# Cria tabelas
Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Dependências

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Injeção de dependências de repositório e serviços
user_repo = UserRepository()
auth_service = AuthService(user_repo)
team_repo = TeamRepository()
team_service = TeamService(team_repo)

router = APIRouter()

# Registro
@router.post("/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Endpoint para registrar novo usuário"""
    created = auth_service.register(db, user)
    return created

# Login
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Endpoint para autenticar usuário e retornar access token"""
    token = auth_service.authenticate(db, form_data.username, form_data.password)
    return {"access_token": token, "token_type": "bearer"}

# Utilitário para pegar user atual
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# CRUD Time
@router.post("/teams", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
def create_team(team: TeamCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    """CRIA um novo time. Apenas usuários autenticados."""
    return team_service.create_team(db, team)

@router.get("/teams", response_model=list[TeamRead])
def list_teams(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    """LISTA todos os times. Apenas usuários autenticados."""
    return team_service.list_teams(db)