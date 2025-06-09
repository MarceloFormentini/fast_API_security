from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from .models import User, Team
from .schemas import UserCreate, TeamCreate

# Interface para repositório de usuários
class IUserRepository(ABC):

    @abstractmethod
    def get_by_username(self, db: Session, username: str) -> User:
        pass

    @abstractmethod
    def create(self, db: Session, user: UserCreate) -> User:
        pass

# Implementação concreta
class UserRepository(IUserRepository):

    def get_by_username(self, db: Session, username: str) -> User:
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, user: UserCreate) -> User:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed = pwd_context.hash(user.password)
        db_user = User(username=user.username, hashed_password=hashed)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

# Interface para repositório de times
class ITeamRepository(ABC):
    @abstractmethod
    def create(self, db: Session, team: TeamCreate) -> Team:
        pass

    @abstractmethod
    def list(self, db: Session) -> list[Team]:
        pass

class TeamRepository(ITeamRepository):

    def create(self, db: Session, team: TeamCreate) -> Team:
        db_team = Team(code=team.code, name=team.name)
        db.add(db_team)
        db.commit()
        db.refresh(db_team)
        return db_team

    def list(self, db: Session) -> list[Team]:
        return db.query(Team).all()