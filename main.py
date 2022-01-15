from flask import request, Response, Blueprint
from .check_signature import verify_signature

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=['POST',])
def check_prs():
    signature_256 = request.headers['X-Hub-Signature-256']
    if not verify_signature(signature_256, request.data):
        return Response(status=403)

    print(request.data)
    
    return Response(status=200)


