import jq

from gh_api import request_api
from const import ROLES, JqStrings


def get_issue_data(
        repo_owner: str,
        repo_name: str,
        issue_number: int,
        sprint_role_option_ids: dict
) -> tuple[str|None, str]:
    result = request_api(f"""query {{
    repository(owner: "{repo_owner}", name: "{repo_name}") {{
        issue(number: {issue_number}) {{
        id
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

    return (sprint_role_option_id, issue_node_id)

