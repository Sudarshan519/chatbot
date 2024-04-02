from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decodeJWT
from jose import jwt

from ai_tools_app.core.config import settings
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        # print(jwtoken)

        try:
            payload = decodeJWT(jwtoken)
            # print(payload)
            # payload1=jwt.decode(jwtoken,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
            # print(payload1)
        except:
            payload = None
        if payload:
            
            isTokenValid = True
        return isTokenValid
    def verify_refresh(self,refresh:str)->bool:
        isTokenValid: bool = False
        # print(jwtoken)

        try:
            payload = decodeJWT(refresh)
            # print(payload)
            # payload1=jwt.decode(jwtoken,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
            # print(payload1)
        except:
            payload = None
        if payload:
            
            isTokenValid = True
        return isTokenValid
    