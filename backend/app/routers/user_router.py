from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_admin
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserSelfUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

# 🔹 Listar todos os usuários (somente admin)
@router.get("/", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    return db.query(User).all()

# 🔹 Criar novo usuário
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password),
        role=user_data.role.upper()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 🔹 Buscar usuário por ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

# 🔹 Atualizar usuário
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Atualiza apenas os campos enviados
    if user_data.name:
        user.name = user_data.name
    if user_data.email:
        # Evita duplicidade de e-mail
        existing = db.query(User).filter(User.email == user_data.email, User.id != user_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="E-mail já está em uso")
        user.email = user_data.email
    if user_data.password:
        from app.core.security import hash_password
        user.password = hash_password(user_data.password)
    if user_data.role:
        user.role = user_data.role.upper()

    db.commit()
    db.refresh(user)
    return user

# 🔹 Deletar usuário
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db.delete(user)
    db.commit()
    return


# 🔹 Atualizar o próprio perfil
@router.put("/me", response_model=UserResponse)
def update_own_profile(
    user_data: UserSelfUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = current_user

    # Atualiza apenas os campos informados
    if user_data.name:
        user.name = user_data.name
    if user_data.email:
        existing = db.query(User).filter(User.email == user_data.email, User.id != user.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="E-mail já está em uso")
        user.email = user_data.email
    if user_data.password:
        from app.core.security import hash_password
        user.password = hash_password(user_data.password)

    db.commit()
    db.refresh(user)
    return user