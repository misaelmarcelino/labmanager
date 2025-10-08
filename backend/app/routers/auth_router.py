from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.models.user import User
from app.schemas.auth_schema import LoginRequest

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
