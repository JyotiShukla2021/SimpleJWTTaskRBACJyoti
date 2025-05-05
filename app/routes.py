from fastapi import APIRouter, Depends, HTTPException
from schemas import UserCreate, UserLogin, Token, ProjectCreate
from models import User, Project
from sqlmodel import Session, select
from auth import get_password_hash, verify_password, create_access_token
from dependencies import get_session, get_current_user, require_role

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_pw = get_password_hash(user.password)
    new_user = User(username=user.username, password=hashed_pw, role=user.role)
    session.add(new_user)
    session.commit()
    return {"message": "User registered successfully"}

@router.post("/login", response_model=Token)
def login(user: UserLogin, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": db_user.username, "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/projects")
def get_projects(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    return session.exec(select(Project)).all()

@router.post("/projects")
def create_project(project: ProjectCreate, session: Session = Depends(get_session), admin: User = Depends(require_role("admin"))):
    new_project = Project(name=project.name, description=project.description)
    session.add(new_project)
    session.commit()
    return new_project
