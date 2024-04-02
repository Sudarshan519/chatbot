#core > security.py

from datetime import datetime,timedelta
from typing import Optional
from jose import JWTError, jwt

from core.config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"]=  (expire)
    print(to_encode)
    
    token = jwt.encode(to_encode,  settings.SECRET_KEY, algorithm='HS256')
 
    decoded=jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
    print(decoded)
    return token

class Authorize:
    @staticmethod
    def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES_IN)
        to_encode["exp"]=  (expire)
 
        
        token = jwt.encode(to_encode,  settings.SECRET_KEY, algorithm='HS256')
 
        decoded=jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
        print(decoded)
        return token