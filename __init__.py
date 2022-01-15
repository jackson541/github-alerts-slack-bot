from flask import Flask, request, Response

secret_access = '7d847723-f866-4ead-9f3a-ffdd26c59e2c'
app = Flask(__name__, instance_relative_config=True)

@app.route('/', methods=['POST',])
def hello():
    signature_256 = request.headers['X-Hub-Signature-256']
    if not verify_signature(secret_access, signature_256, request.data):
        return Response(status=403)
    return Response(status=200)





import hmac

def verify_signature(key, signature, body):
    digest = hmac.new(key.encode("ascii"), msg=body, digestmod="sha256")
    return hmac.compare_digest(f"sha256={digest.hexdigest().lower()}", signature.lower())
