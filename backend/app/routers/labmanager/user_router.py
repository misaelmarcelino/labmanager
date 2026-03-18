import secrets, string
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from app.core.labmanager.database import get_db
from app.core.labmanager.dependencies import get_current_user, require_admin
from app.core.labmanager.security import hash_password
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserSelfUpdate, UserResponse
from app.services.mail_service import send_welcome_email
from app.shared.config.labmanager.logging import logging

router = APIRouter(prefix="/users", tags=["Usuários"])


# 🧩 Utilitário para gerar senha aleatória
def generate_temp_password(length: int = 10) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%&*"
    return "".join(secrets.choice(alphabet) for _ in range(length))


# 🔹 Listar todos os usuários (somente ADMIN)
@router.get("/", response_model=List[UserResponse], summary="Listar todos os usuários (apenas admin)")
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    users = db.query(User).all()
    return users


# 🔹 Criar novo usuário
@router.post("/", status_code=status.HTTP_201_CREATED, summary="Criar novo usuário (apenas admin)")
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    # Verifica duplicidade
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    temp_password = generate_temp_password()

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(temp_password),
        role=user_data.role.value.upper(),
        is_first_access=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Envio de e-mail de boas-vindas
    try:
        send_welcome_email(new_user.email, new_user.name, temp_password) #type: ignore
        email_status = "E-mail de acesso enviado ao colaborador."
    except Exception as e:
        logging.error(f"⚠️ Erro ao enviar e-mail: {e}")
        # print(f"⚠️ Erro ao enviar e-mail: {e}")
        email_status = "Usuário criado, mas houve erro ao enviar o e-mail."

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": f"Usuário criado com sucesso! {email_status}",
            "user": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "role": new_user.role
            }
        }
    )


# 🔹 Obter informações do próprio perfil
@router.get("/users/me", response_model=UserResponse, summary="Obter informações do próprio perfil")
def get_own_profile(current_user: User = Depends(get_current_user)):
    """
    Retorna as informações do colaborador autenticado com base no token JWT.
    """
    return current_user

# 🔹 Atualizar o próprio perfil
@router.put("/me", response_model=UserResponse, summary="Atualizar o próprio perfil")
def update_own_profile( #type: ignore
    user_data: UserSelfUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if user_data.name:
        current_user.name = user_data.name #type: ignore
    if user_data.email:
        existing = db.query(User).filter(User.email == user_data.email, User.id != current_user.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="E-mail já está em uso")
        current_user.email = user_data.email #type: ignore
    if user_data.password:
        current_user.password = hash_password(user_data.password) #type: ignore

    db.commit()
    db.refresh(current_user)
    return current_user

# 🔹 Atualizar usuário (ADMIN)
@router.put("/{user_id}", response_model=UserResponse, summary="Atualizar usuário existente (apenas admin)")
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Atualiza apenas campos fornecidos
    if user_data.name:
        user.name = user_data.name #type: ignore
    if user_data.email:
        existing = db.query(User).filter(User.email == user_data.email, User.id != user_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="E-mail já está em uso")
        user.email = user_data.email #type: ignore
    if user_data.password:
        user.password = hash_password(user_data.password) #type: ignore
    if user_data.role:
        user.role = user_data.role.value.upper() #type: ignore

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Excluir usuário (apenas admin)")
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
    return Response(status_code=status.HTTP_204_NO_CONTENT)




# 🔹 Atualizar o próprio perfil
@router.put("/me", response_model=UserResponse, summary="Atualizar o próprio perfil")
def update_own_profile(
    user_data: UserSelfUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if user_data.name:
        current_user.name = user_data.name #type: ignore
    if user_data.email:
        existing = db.query(User).filter(User.email == user_data.email, User.id != current_user.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="E-mail já está em uso")
        current_user.email = user_data.email #type: ignore
    if user_data.password:
        current_user.password = hash_password(user_data.password) #type: ignore

    db.commit()
    db.refresh(current_user)
    return current_user
