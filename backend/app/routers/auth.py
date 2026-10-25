from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from jose import jwt

from app.config import settings
from app.db import users_col
from app.deps import get_current_user
from app.models.user import GoogleAuthRequest, UserOut, TokenOut

router = APIRouter(prefix="/auth", tags=["auth"])


def _create_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    return jwt.encode(
        {"sub": user_id, "exp": expire},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )


@router.post("/google", response_model=TokenOut)
async def google_auth(body: GoogleAuthRequest):
    try:
        audience = settings.GOOGLE_CLIENT_ID
        id_info = id_token.verify_oauth2_token(
            body.credential,
            google_requests.Request(),
            audience,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google token: {str(e)}",
        )

    email = id_info.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google token missing email",
        )

    name = id_info.get("name")
    picture = id_info.get("picture")
    google_id = id_info.get("sub")

    user = await users_col.find_one({"email": email})
    if not user:
        doc = {
            "email": email,
            "name": name,
            "picture": picture,
            "google_id": google_id,
            "created_at": datetime.utcnow(),
        }
        res = await users_col.insert_one(doc)
        user_id = str(res.inserted_id)
    else:
        user_id = str(user["_id"])
        await users_col.update_one(
            {"_id": user["_id"]},
            {"$set": {"name": name, "picture": picture, "google_id": google_id}},
        )

    token = _create_token(user_id)
    return TokenOut(access_token=token)


@router.get("/me", response_model=UserOut)
async def get_me(user: dict = Depends(get_current_user)):
    return UserOut(
        id=user["id"],
        email=user["email"],
        name=user.get("name"),
        picture=user.get("picture"),
        created_at=user.get("created_at") or datetime.utcnow(),
    )
