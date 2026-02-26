import jq

from gh_api import request_api
from const import ROLES, JqStrings


def get_pr_data(
        repo_owner: str,
        repo_name: str,
        pr_number: int,
) -> str:
    result = request_api(f"""query {{
    repository(owner: "{repo_owner}", name: "{repo_name}") {{
        pullRequest(number: {pr_number}) {{
            id
        }}
    }}
    }}""")

    pr_node_id = jq.compile(JqStrings.GET_PR_NODE_ID).input_value(result).first()
    return pr_node_id
