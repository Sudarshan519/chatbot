import time
from typing import Dict

from jose import jwt
 
from ai_tools_app.core.config import settings

JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = settings.ALGORITHM


def token_response(token: str):
    return {
        "access_token": token
    }

# function used for signing the JWT string
def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "exp": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        # print(time.time())
        # print(decoded_token)
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except Exception as e:
        print(e)
        return {}