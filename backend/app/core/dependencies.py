from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from jose import JWTError
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User

oauth2_scheme = HTTPBearer()


# ✅ Obtém o usuário autenticado a partir do token
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return user


# ✅ Restrição apenas para administradores
def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role.upper() != "ADMIN":
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
    return current_user


# ✅ Restrição apenas para usuários comuns
def require_user(current_user: User = Depends(get_current_user)):
    if current_user.role.upper() != "USER":
        raise HTTPException(status_code=403, detail="Acesso restrito a usuários padrão")
    return current_user


# ✅ Restrição dinâmica para múltiplos papéis
def role_required(*roles: str):
    """
    Permite múltiplos papéis, exemplo:
    @Depends(role_required("ADMIN", "SUPERVISOR"))
    """
    def wrapper(current_user: User = Depends(get_current_user)):
        if current_user.role.upper() not in [r.upper() for r in roles]:
            raise HTTPException(status_code=403, detail="Acesso negado a este papel")
        return current_user
    return wrapper
