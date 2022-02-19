from typing import Optional, MutableMapping, List, Union
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from jose import jwt
# https://github.com/mpdavis/python-jose

from app.models.user import User
from app.core.config import settings
from app.core.security import verify_password

JWTPayloadMapping = MutableMapping[
    str, Union[datetime, bool, str, List[str], List[int]]
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def authenticate(
        *,
        email: str,
        password: str,
        db: Session,
) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(*, sub: str) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _create_token(
        token_type: str,
        lifetime: timedelta,
        sub: str,
) -> str:
    payload = {}
    # required/optional fields https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire  # expiration datetime
    payload["iat"] = datetime.utcnow()  # issued at
    payload["sub"] = str(sub)  # subject of the JWT. In this case, a user ID

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
