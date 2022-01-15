import hmac
from .constants import *

def verify_signature(signature, body):
    digest = hmac.new(SECRET_ACCESS.encode("ascii"), msg=body, digestmod="sha256")
    return hmac.compare_digest(f"sha256={digest.hexdigest().lower()}", signature.lower())
