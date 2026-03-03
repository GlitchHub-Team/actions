"""
Tutte le funzioni relative alle Issue
"""

import jq

from gh_api import request_api
from const import ROLES, JqStrings, PARENT_ISSUES


def get_issue_data(
        repo_owner: str,
        repo_name: str,
        issue_number: int,
        sprint_role_option_ids: dict
) -> tuple[str|None, str, str]:
    result = request_api(f"""query {{
    repository(owner: "{repo_owner}", name: "{repo_name}") {{
        issue(number: {issue_number}) {{
        id
        title
        labels(first: 50) {{
            nodes {{ name }}
        }}
        }}
    }}
    }}""")

    label_presences = {}
    for role in ROLES:
        label_name = f"task-{role.lower()}"
        print(f"  -> searching for {label_name}...")
        label_presences[role] = bool(jq.compile(JqStrings.GET_LABEL_ID % label_name).input_value(result).all())

    sprint_role_option_id = None
    for role in ROLES:
        if label_presences[role]:
            print(f"  RUOLO: {role}")
            sprint_role_option_id = sprint_role_option_ids[role]
            break
    else:
        print("  RUOLO: nessun ruolo trovato")
    
    issue_node_id = jq.compile(JqStrings.GET_ISSUE_NODE_ID).input_value(result).first()

    issue_title = jq.compile(JqStrings.GET_ISSUE_TITLE).input_value(result).first()

    return (sprint_role_option_id, issue_node_id, issue_title)


def get_parent_issue_from_title(issue_title: str) -> tuple[str, str, int]|None:
    issue_title = issue_title.strip().lower()

    for scope, issue_number in PARENT_ISSUES.items():
        if issue_title.startswith(f"[{scope}]"):
            return issue_number
    
    return None


def set_parent_issue(
        issue_node_id: str,
        parent_issue_node_id: str,
):
    request_api(f"""mutation {{
    addSubIssue(input: {{
        issueId: "{parent_issue_node_id}"
        subIssueId: "{issue_node_id}"
        replaceParent: false
    }})
    }}""")