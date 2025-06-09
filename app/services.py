from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .config import settings
from .repositories import IUserRepository, ITeamRepository
from .schemas import UserCreate, TeamCreate

class AuthService:
    def __init__(self, repo: IUserRepository):  # DIP: depende da abstração
        self.repo = repo

    def register(self, db: Session, user: UserCreate):
        existing = self.repo.get_by_username(db, user.username)
        if existing:
            raise HTTPException(status_code=400, detail="Username already registered")
        return self.repo.create(db, user)

    def authenticate(self, db: Session, username: str, password: str) -> str:
        user = self.repo.get_by_username(db, username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        if not pwd_context.verify(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        # Gera JWT
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"sub": user.username, "exp": expire}
        token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return token

class TeamService:
    def __init__(self, repo: ITeamRepository):
        self.repo = repo

    def create_team(self, db: Session, team: TeamCreate):
        return self.repo.create(db, team)

    def list_teams(self, db: Session):
        return self.repo.list(db)