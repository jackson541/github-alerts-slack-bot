from github import Github
from .constants import *
import requests
import json
import time
import redis
from urllib.parse import urlparse

# using an access token
g = Github(ACCESS_TOKEN)
repo = g.get_repo(PROJECT_TO_TRACK)

if REDIS_URL:
    url = urlparse(REDIS_URL)
    redis_var = redis.Redis(host=url.hostname, port=url.port, password=url.password)
else:
    redis_var = redis.Redis(host='localhost', port=6379, db=0)


def check_pr_branch_is_correct(request_data: dict):
    """
    Check if branch destination of PR in webhook is same of BRANCH_TO_TRACK

    - request_data [dict]: body of request to API
    """
    return request_data['pull_request']['base']['ref'] == BRANCH_TO_TRACK
    

def get_not_mergeable_prs():
    """
    Search for PRs with conflicts
    """
    not_mergeable_prs = []

    pulls = repo.get_pulls(state='open', sort='created', base=BRANCH_TO_TRACK)
    for pr in pulls:
        pr_detail = repo.get_pull(pr.number)
        if pr_detail.mergeable == None:
            """ After merge a PR into BRANCH_TO_TRACK, GitHub set all others PRs opens to it with mergeable = None.
            So, is necessary send a request for this PRs and await some time to GitHub calculated again mergeable of they. """
            time.sleep(2)
            pr_detail = repo.get_pull(pr.number)

        if not pr_detail.mergeable and pr_detail.mergeable != None: 
            not_mergeable_prs.append(str(pr.number))

    return not_mergeable_prs


def check_there_are_new_not_mergeable_pr(not_mergeable_prs: list):
    """
    Check if in the list of PRs with conflicts there are any new PR

    - not_mergeable_prs [array]: list of Pull Resquest IDs in string format
    """
    old_prs_in_byte = redis_var.get('prs_conflicts')
    old_prs_with_conflicts = old_prs_in_byte.decode('utf-8').split(',') if old_prs_in_byte else list()

    new_prs_in_conflict = list(set(not_mergeable_prs) - set(old_prs_with_conflicts))
    if not new_prs_in_conflict:
        return False
    
    concated_list_prs = ','.join(new_prs_in_conflict + old_prs_with_conflicts)
    redis_var.setex('prs_conflicts', ONE_DAY_IN_SECONDS, bytes(concated_list_prs, encoding='utf-8'))
    return True


def notify_not_mergeable_prs_in_slack(not_mergeable_prs: list):
    """
    Send notification to slack with the IDs of PRs with conflicts

    - not_mergeable_prs [array]: list of Pull Resquest IDs in string format
    """
    data = {
        'prs_list': ', '.join(not_mergeable_prs)
    }

    requests.post(SLACK_WEBHOOK_LINK, data=json.dumps(data))
