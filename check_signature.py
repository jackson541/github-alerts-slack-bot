import hmac
secret_access = '7d847723-f866-4ead-9f3a-ffdd26c59e2c'

def verify_signature(signature, body):
    digest = hmac.new(secret_access.encode("ascii"), msg=body, digestmod="sha256")
    return hmac.compare_digest(f"sha256={digest.hexdigest().lower()}", signature.lower())
