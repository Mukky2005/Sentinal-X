import time
import hmac
import hashlib
import json
import base64
from typing import Optional, Dict, Any
from fastapi import HTTPException, Header, Depends
from .config import SECRET_KEY, ALGORITHM

def b64_url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def b64_url_decode(s: str) -> bytes:
    padding = '=' * (4 - (len(s) % 4))
    return base64.urlsafe_b64decode(s + padding)

class TokenManager:
    """
    Zero-Trust Token Management (NIST SP 800-207 & OAuth 2.0 RFC 9700 BCP)
    Signs and verifies tenant-bound JWT tokens with signature validation.
    """
    def __init__(self, secret: str = SECRET_KEY):
        self.secret = secret.encode('utf-8')

    def create_access_token(self, payload: Dict[str, Any], expires_in_seconds: int = 86400) -> str:
        header = {"alg": "HS256", "typ": "JWT"}
        body = payload.copy()
        body["exp"] = int(time.time()) + expires_in_seconds
        body["iat"] = int(time.time())
        body["iss"] = "sentinelx-auth-gate"

        header_b64 = b64_url_encode(json.dumps(header).encode('utf-8'))
        body_b64 = b64_url_encode(json.dumps(body).encode('utf-8'))
        signing_input = f"{header_b64}.{body_b64}".encode('utf-8')
        signature = hmac.new(self.secret, signing_input, hashlib.sha256).digest()
        sig_b64 = b64_url_encode(signature)

        return f"{header_b64}.{body_b64}.{sig_b64}"

    def verify_token(self, token: str) -> Dict[str, Any]:
        try:
            parts = token.split('.')
            if len(parts) != 3:
                raise ValueError("Invalid token segments")
            header_b64, body_b64, sig_b64 = parts
            signing_input = f"{header_b64}.{body_b64}".encode('utf-8')
            expected_sig = hmac.new(self.secret, signing_input, hashlib.sha256).digest()
            actual_sig = b64_url_decode(sig_b64)

            if not hmac.compare_digest(expected_sig, actual_sig):
                raise ValueError("Token signature verification failed")

            body = json.loads(b64_url_decode(body_b64).decode('utf-8'))
            if body.get("exp", 0) < time.time():
                raise ValueError("Token expired")

            return body
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")

token_manager = TokenManager()

def get_current_user_claims(authorization: Optional[str] = Header(None)) -> Optional[Dict[str, Any]]:
    """FastAPI Dependency for server-side token resolution"""
    if not authorization:
        return None
    scheme, _, token = authorization.partition(' ')
    if scheme.lower() != 'bearer' or not token:
        return None
    return token_manager.verify_token(token)
