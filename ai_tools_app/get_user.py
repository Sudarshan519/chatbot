import secrets
from typing import Annotated

from fastapi import security
from ai_tools_app.db.session import get_db
from ai_tools_app.models.user import AdminUser
from ai_tools_app.core.config import settings
from fastapi.security import HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from fastapi import Depends, HTTPException, Response,status
from sqlmodel import Session
 
from ai_tools_app.core.jwt_bearer import JWTBearer
# Get user from database
def get_user(username:str,db: Session):
    user = db.query(AdminUser).filter(AdminUser.email == username).first()
    return user

 
def get_current_user_from_bearer( jwtb: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            jwtb, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        ) 
 
        
        username: str = payload.get("sub")

        return get_user(username=username, db=db)
 
    except JWTError as e:
        return credentials_exception



def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"stanleyjobson"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"swordfish"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

