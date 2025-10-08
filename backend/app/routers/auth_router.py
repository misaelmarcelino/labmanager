from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, create_access_token, hash_password
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth_schema import LoginRequest, ChangePasswordRequest, ChangePasswordResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
        )

    token = create_access_token({
        "sub": user.email,
        "name": user.name,
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "name": user.name,
        "email": user.email,
        "role": user.role
    }


@router.put("/change-password", response_model=ChangePasswordResponse)
def change_password(
    data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1️⃣ Verifica senha atual
    if not verify_password(data.old_password, current_user.password):
        raise HTTPException(status_code=400, detail="Senha atual incorreta")

    # 2️⃣ Valida se a nova senha é diferente da anterior
    if data.old_password == data.new_password:
        raise HTTPException(status_code=400, detail="A nova senha deve ser diferente da atual")

    # 3️⃣ Atualiza a senha
    current_user.password = hash_password(data.new_password)
    db.commit()
    db.refresh(current_user)

    return {"message": "Senha alterada com sucesso!"}