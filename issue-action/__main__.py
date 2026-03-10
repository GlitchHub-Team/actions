import argparse
import jq
import re

from issue import get_issue_data, get_parent_issue_from_title, set_parent_issue
from pr import get_pr_data, link_issue
from project import get_project_data, set_sprint_iteration, set_sprint_role, add_to_project

from const import ISSUE_BRANCH_PREFIX, ISSUE_BRANCH_GET_NUMBER_REGEX

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
        "--set-parent",
        action="store_true",
        help="Imposta la parent issue leggendo il titolo dell'issue. Ignorato se il parametro --pr è impostato."
    )

    parser.add_argument(
        "--pr",
        action="store_true",
        help="Da usare se i dati inseriti sono relativi a una PR e non una Issue"
    )

    parser.add_argument(
        "--link-issue",
        action="store_true",
        help="Se parametro --pr è impostato, allora crea link dalla PR a relativa issue"
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

    # Se è una PR:
    if args.pr:
        print("::notice::[PROCEDURA PR]")
        print("::notice::get_pr_data...")
        pr_node_id, ref_name, pr_body = get_pr_data(repo_owner, repo_name, issue_or_pr_number)
        
        print("::notice::add_to_project...")
        item_id = add_to_project(project_id, pr_node_id)

        if args.iteration:
            print("::notice::set_sprint_iteration...")
            set_sprint_iteration(
                project_id,
                item_id,
                sprint_field_id,
                current_iter_option_id
            )

        if args.role:
            print("::notice::set_sprint_role... (verificatore)")
            set_sprint_role(
                project_id,
                item_id,
                sprint_role_field_id,
                sprint_role_option_ids["Verificatore"],
            )
        
        if args.link_issue:
            print("::notice::link_issue_with_comment...")
            if ref_name.startswith(ISSUE_BRANCH_PREFIX):
                issue_number = int(re.findall(ISSUE_BRANCH_GET_NUMBER_REGEX, ref_name)[0])
                link_issue(pr_body, pr_node_id, issue_number)
            else:
                print(f"::notice::  -> issue branch not found")

    # Se è un'issue:
    else:
        print("::notice::[PROCEDURA ISSUE]")
        print("::notice::get_issue_data...")
        sprint_role_option_id, issue_node_id, issue_title = get_issue_data(repo_owner, repo_name, issue_or_pr_number, sprint_role_option_ids)

        print("::notice::add_to_project...")
        item_id = add_to_project(project_id, issue_node_id)
        
        if args.set_parent:
            print("get_parent_issue_from_title...")
            parent_issue = get_parent_issue_from_title(issue_title)
            if parent_issue:
                print(f"  -> parent_issue: #{parent_issue}")
                print("get_issue_data (parent issue)...")
                _, parent_issue_node_id, _ = get_issue_data(*parent_issue, {})
                
                print("set_parent_issue...")
                try:
                    set_parent_issue(issue_node_id, parent_issue_node_id)
                except:
                    print("::warning::La issue ha già un parent")

        if args.iteration:
            print("::notice::set_sprint_iteration...")
            set_sprint_iteration(
                project_id,
                item_id,
                sprint_field_id,
                current_iter_option_id
            )

        if args.role:
            print("::notice::set_sprint_role...")
            set_sprint_role(
                project_id,
                item_id,
                sprint_role_field_id,
                sprint_role_option_id,
            )

        print("::notice::Script eseguito con successo!")


if __name__ == "__main__":
    main()    
