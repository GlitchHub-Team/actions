"""
Tutte le funzioni relative alle Pull Request
"""

import jq

from gh_api import request_api
from const import ROLES, JqStrings


def get_pr_data(
        repo_owner: str,
        repo_name: str,
        pr_number: int,
) -> tuple[str, str, str]:
    result = request_api(f"""query {{
        repository(owner: "{repo_owner}", name: "{repo_name}") {{
            pullRequest(number: {pr_number}) {{
                id
                headRefName
                body
            }}
        }}
    }}""")

    pr_node_id  = jq.compile(JqStrings.GET_PR_NODE_ID).input_value(result).first()
    ref_name    = jq.compile(JqStrings.GET_PR_REF_NAME).input_value(result).first()
    body        = jq.compile(JqStrings.GET_PR_COMMENTS).input_value(result).first()

    return pr_node_id, ref_name, body

def link_issue(
        previous_body: str,
        pr_node_id: str,
        issue_number: int
):

    if f"closes #{issue_number}" in previous_body:
        print(f"  -> close message already present")
        return

    new_body = fr"{previous_body.strip('"')}\n\ncloses #{issue_number}"

    request_api(f"""mutation {{
        updatePullRequest(input: {{
            pullRequestId: "{pr_node_id}"
            body: "{new_body}"
        }}) {{
            clientMutationId
        }}
    }}""")
    print(f"  -> linked issue #issue_number")