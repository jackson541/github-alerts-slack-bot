from flask import request, Response, Blueprint
from .check_signature import verify_signature
from .funcs import check_pr_branch_is_correct, get_not_mergeable_prs, notify_not_mergeable_prs_in_slack
import json

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=['POST',])
def check_prs():
    signature_256 = request.headers['X-Hub-Signature-256']
    if not verify_signature(signature_256, request.data):
        return Response(status=403)

    if not check_pr_branch_is_correct(json.loads(request.data)):
        return Response(status=200)

    not_mergeable_prs = get_not_mergeable_prs()

    if not_mergeable_prs:
        notify_not_mergeable_prs_in_slack(not_mergeable_prs)
    else:
        print('all opens PRs are OK!')

    return Response(status=200)


