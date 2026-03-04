from github import Github, Auth, Branch, Repository
from github.GithubException import UnknownObjectException

import argparse
import os
import re

def delete_branch(repo: Repository.Repository, branch_name: str):
    try:
        ref = repo.get_git_ref(f"heads/{branch_name}")
        ref.delete()
        print(f"::debug title=delete_branch::Eliminato branch: {branch_name}")
    except UnknownObjectException:
        print(f"::warning title=delete_branch::Branch {branch_name} non esiste")


GH = Github(auth=Auth.Token(os.environ["GH_TOKEN"]))

def main():
  
    parser = argparse.ArgumentParser(
        prog="delete-issue-branches"
    )

    parser.add_argument(
        "repo",
        help="Nome della repository nella forma REPO_OWNER/REPO_NAME"
    )

    parser.add_argument(
        "pr_ref",
        type=str,
        help="Gitref della PR da eliminare oltre a PR vecchie"
    )

    args = parser.parse_args()

    if not args.pr_to_close:
        print("::error::Numero PR invalido")
        exit(1)

    repo = GH.get_repo(args.repo)

    issue_branches: dict[int, Branch.Branch] = {}

    print("::notice::Eliminazione issue branch vecchi...")
    for branch in repo.get_branches():
        if (match := re.findall(r"^issue-(\d+)$", branch.name)):
            issue_num = int(match[0])
            issue_branches[issue_num] = branch

    for issue_number, branch in issue_branches.items():
        try:
            issue = repo.get_issue(issue_number)
            if issue.state == "closed":
                delete_branch(repo, branch.name)

        except UnknownObjectException:
            print(f"::warning::Trovato branch {branch.name} ma non issue #{issue_number}")

    print("::notice::Eliminazione issue branch corrente...")
    try:
        issue = repo.get_issue(args.pr_to_close)
        if issue.state == "closed":
            delete_branch(repo, f"issue-{args.pr_to_close}")

    except UnknownObjectException:
        print(f"::warning::Branch 'issue-{args.pr_to_close}' non trovato")


if __name__ == "__main__":
    main()