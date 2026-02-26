import argparse
import jq

from issue import get_issue_data
from pr import get_pr_data
from project import get_project_data, set_sprint_iteration, set_sprint_role, add_to_project

def main():
    parser = argparse.ArgumentParser(
        prog="GlitchHub-Team Issue Automation",
        description="Automazione per gestione issue/PR di GlitchHub-Team"
    )

    parser.add_argument(
        "project",
        help="Identificativo GH Project nella forma OWNER/PROJECT_ID"
    )

    parser.add_argument(
        "issue_or_pr", type=str,
        help="Identificativo issue nella forma REPO_OWNER/REPO_NAME/ISSUE_OR_PR_NUMBER"
    )

    parser.add_argument(
        "--iteration",
        action="store_true",
        help="Imposta il campo Sprint Iteration corrente nell'issue"
    )

    parser.add_argument(
        "--role",
        action="store_true",
        help="Imposta il campo Sprint role nell'issue. Se il parametro --pr è impostato, mette sempre il ruolo Verificatore."
    )

    parser.add_argument(
        "--pr",
        action="store_true",
        help="Da usare se i dati inseriti sono relativi a una PR e non una Issue"
    )

    args = parser.parse_args()

    try:
        project_organization, project_number = args.project.strip(' "').split("/")
    except ValueError:
        print("ERROR: Il parametro project dev'essere nella forma OWNER/PROJECT_ID")
        exit(1)

    try:
        repo_owner, repo_name, issue_or_pr_number = args.issue_or_pr.strip(' "').split("/")
    except ValueError:
        print("ERROR: Il parametro issue dev'essere nella forma REPO_OWNER/REPO_NAME/ISSUE_OR_PR_NUMBER")
        exit(1)

    print("get_project_data...")
    (
        project_id,
        sprint_field_id,
        current_iter_option_id,
        sprint_role_field_id,
        sprint_role_option_ids
    ) = get_project_data(project_organization, project_number)

    if args.pr:
        print("[PROCEDURA PR]")
        print("get_pr_data...")
        pr_node_id = get_pr_data(repo_owner, repo_name, issue_or_pr_number)
        
        print("add_to_project...")
        item_id = add_to_project(project_id, pr_node_id)

        if args.iteration:
            print("set_sprint_iteration...")
            set_sprint_iteration(
                project_id,
                item_id,
                sprint_field_id,
                current_iter_option_id
            )

        if args.role:
            print("set_sprint_role... (verificatore)")
            set_sprint_role(
                project_id,
                item_id,
                sprint_role_field_id,
                sprint_role_option_ids["Verificatore"],
            )

    else:
        print("[PROCEDURA ISSUE]")
        print("get_issue_data...")
        sprint_role_option_id, issue_node_id = get_issue_data(repo_owner, repo_name, issue_or_pr_number, sprint_role_option_ids)

        print("add_to_project...")
        item_id = add_to_project(project_id, issue_node_id)
        
        if args.iteration:
            print("set_sprint_iteration...")
            set_sprint_iteration(
                project_id,
                item_id,
                sprint_field_id,
                current_iter_option_id
            )

        if args.role:
            print("set_sprint_role...")
            set_sprint_role(
                project_id,
                item_id,
                sprint_role_field_id,
                sprint_role_option_id,
            )

        print("Script eseguito con successo")


if __name__ == "__main__":
    main()    
