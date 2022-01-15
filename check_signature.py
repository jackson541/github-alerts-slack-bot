import hmac
from .constants import *

def verify_signature(signature: str, body: bytes):
    """
    Verify if call of API comes from correct project of github 
    """
    digest = hmac.new(SECRET_ACCESS.encode("ascii"), msg=body, digestmod="sha256")
    return hmac.compare_digest(f"sha256={digest.hexdigest().lower()}", signature.lower())
