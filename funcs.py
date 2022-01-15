from github import Github
from .constants import *
import requests
import json
import time

# using an access token
g = Github(ACCESS_TOKEN)
repo = g.get_repo(PROJECT_TO_TRACK)

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
            """ After merge a PR into BRANCH_TO_TRACK, github set all others PRs opens to it with mergeable = None.
            So, is necessary send a request for this PRs and await some time to GitHub calculated again mergeable of they. """
            time.sleep(2)
            pr_detail = repo.get_pull(pr.number)

        if not pr_detail.mergeable and pr_detail.mergeable != None: 
            not_mergeable_prs.append(str(pr.number))
            print(pr.number, pr_detail.mergeable, pr_detail.mergeable_state)

    return not_mergeable_prs


def notify_not_mergeable_prs_in_slack(not_mergeable_prs: list):
    """
    Send notification to slack with de number of PRs with conflicts

    - not_mergeable_prs [array]: list of Pull Resquest IDs in string format
    """
    data = {
        'prs_list': ', '.join(not_mergeable_prs)
    }

    requests.post(SLACK_WEBHOOK_LINK, data=json.dumps(data))
