import jq

from gh_api import request_api
from typing import Literal

from const import JqStrings, ROLES, RoleStr



def add_to_project(
        project_id: str,
        issue_or_pr_node_id: str
) -> str:
    result = request_api(f"""mutation {{
        addProjectV2ItemById(input: {{projectId: "{project_id}", contentId: "{issue_or_pr_node_id}"}}) {{
            item {{id}}
        }}
    }}""")
    
    item_id = jq.compile(JqStrings.GET_PROJECT_ITEM_ID).input_value(result).first()
    return item_id


def get_project_data(
        organization: str,
        project_number: int
) -> tuple[str, str, str, str, dict[RoleStr, str]]:
    result = request_api(f"""query {{ 
        organization(login: "{organization}"){{ 
        projectV2(number: {project_number}) {{ 
            id 
            fields(first:50) {{ 
            nodes {{ 
                ... on ProjectV2Field {{ 
                    id 
                    name 
                }}
                ... on ProjectV2IterationField {{
                    id
                    name
                    configuration {{
                        completedIterations {{
                            title
                            startDate
                            id
                        }}
                        iterations {{
                            title
                            startDate
                            id
                        }}
                    }}
                }}
                ... on ProjectV2SingleSelectField {{ 
                    id 
                    name 
                    options {{ 
                        id 
                        name 
                    }} 
                }}
            }} 
            }} 
        }} 
        }} 
    }}""")

    project_id              = jq.compile(JqStrings.GET_PROJECT_ID).input_value(result).first()
    sprint_field_id         = jq.compile(JqStrings.GET_SPRINT_FIELD_ID).input_value(result).first()
    current_iter_option_id  = jq.compile(JqStrings.GET_CUR_ITER_OPTION_ID).input_value(result).first()
    sprint_role_field_id    = jq.compile(JqStrings.GET_SPRINT_ROLE_FIELD_ID).input_value(result).first()

    sprint_role_option_ids = {}
    for role in ROLES:
        sprint_role_option_ids[role] = jq.compile(JqStrings.GET_ROLE_OPTION_ID % role).input_value(result).first()

    return (
        project_id,
        sprint_field_id,
        current_iter_option_id,
        sprint_role_field_id,
        sprint_role_option_ids
    )



def set_sprint_iteration(
        project_id: str,
        item_id: str,
        sprint_field_id: str,
        current_iteration_option_id: str|None,
):
    if not current_iteration_option_id:
        print(f"ERRORE: Nel GitHub Project non esiste il valore del campo Sprint legato all'iterazione corrente."
              " Per far funzionare l'automation, si prega di crearlo nelle impostazioni del GitHub Project.")
        return exit(1)
 
    print(f"  -> current_iteration_option_id = {current_iteration_option_id}")

    result = request_api(f"""mutation {{
        updateProjectV2ItemFieldValue(input: {{
            projectId: "{project_id}"
            itemId: "{item_id}"
            fieldId: "{sprint_field_id}"
            value: {{ iterationId: "{current_iteration_option_id}" }}
        }}) {{
            projectV2Item {{id}}
        }}
    }}""")


def set_sprint_role(
        project_id: str,
        item_id: str,
        sprint_role_field_id: str,
        sprint_role_option_id: str|None,
):
    # Set non-empty sprint role 
    if sprint_role_option_id:
        print(f"  -> sprint_role_option_id = {sprint_role_option_id}")
        request_api(f"""mutation {{
            updateProjectV2ItemFieldValue(input: {{
                projectId: "{project_id}"
                itemId: "{item_id}"
                fieldId: "{sprint_role_field_id}"
                value: {{ singleSelectOptionId: "{sprint_role_option_id}" }}
            }}) {{
                projectV2Item {{id}}
            }}
        }}""")
    
    # Set empty sprint role
    else:
        print(f"  -> rimuovo lo Sprint Role")
        request_api(f"""mutation {{
            clearProjectV2ItemFieldValue(input: {{
            projectId: "{project_id}"
            itemId: "{item_id}"
            fieldId: "{sprint_role_field_id}"
            }}) {{
                projectV2Item {{id}}
            }}
        }}""")