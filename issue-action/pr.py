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
) -> tuple[str, str, list]:
    result = request_api(f"""query {{
        repository(owner: "{repo_owner}", name: "{repo_name}") {{
            pullRequest(number: {pr_number}) {{
                id
                headRefName
                comments(first: 50) {{
                    nodes {{ body }}
                }}
            }}
        }}
    }}""")

    pr_node_id = jq.compile(JqStrings.GET_PR_NODE_ID).input_value(result).first()
    ref_name = jq.compile(JqStrings.GET_PR_REF_NAME).input_value(result).first()
    comments = jq.compile(JqStrings.GET_PR_COMMENTS).input_value(result).first()

    return pr_node_id, ref_name, comments

def link_issue_with_comment(
        previous_comments: list,
        pr_node_id: str,
        issue_number: int
):

    for comment in previous_comments:
        if f"closes #{issue_number}" in comment["body"]:
            print(f"  -> close comment already present")
            return

    request_api(f"""mutation {{
        addComment(input: {{
            subjectId: "{pr_node_id}"
            body: "closes #{issue_number}"
        }}) {{
            clientMutationId
        }}
    }}""")
    print(f"  -> linked issue #issue_number")