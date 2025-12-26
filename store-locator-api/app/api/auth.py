from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.deps import get_db
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest, LogoutRequest
from app.auth.security import verify_password, make_access_token, make_refresh_token, hash_token

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email, User.status == "active").first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access = make_access_token(user.user_id, user.email, user.role)
    refresh_raw, refresh_exp = make_refresh_token(user.user_id)

    db.add(RefreshToken(
        token_hash=hash_token(refresh_raw),
        user_id=user.user_id,
        expires_at=refresh_exp,
        revoked=False,
    ))
    db.commit()

    return TokenResponse(access_token=access, refresh_token=refresh_raw)

@router.post("/refresh")
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    th = hash_token(payload.refresh_token)
    rt = db.query(RefreshToken).filter(RefreshToken.token_hash == th).first()
    if not rt or rt.revoked or rt.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = db.query(User).filter(User.user_id == rt.user_id, User.status == "active").first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    access = make_access_token(user.user_id, user.email, user.role)
    return {"access_token": access}

@router.post("/logout")
def logout(payload: LogoutRequest, db: Session = Depends(get_db)):
    th = hash_token(payload.refresh_token)
    rt = db.query(RefreshToken).filter(RefreshToken.token_hash == th).first()
    if rt:
        rt.revoked = True
        db.commit()
    return {"ok": True}