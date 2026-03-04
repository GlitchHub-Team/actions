import os

from typing import Literal, TypeAlias

URL = "https://api.github.com/graphql"
try:
    GH_TOKEN = os.environ["GH_TOKEN"]
except IndexError:
    print("Token GitHub action non impostato nella variable env GH_TOKEN")
    exit(1)

class JqStrings:
    GET_PROJECT_ID              = '.data.organization.projectV2.id'
    GET_SPRINT_FIELD_ID         = '.data.organization.projectV2.fields.nodes[] | select(.name== "Sprint") | .id'
    GET_CUR_ITER_OPTION_ID      = '.data.organization.projectV2.fields.nodes[] | select(.name == "Sprint") | .configuration.iterations | first | .id'
    GET_SPRINT_ROLE_FIELD_ID    = '.data.organization.projectV2.fields.nodes[] | select(.name== "Sprint role") | .id'

    GET_ROLE_OPTION_ID  = '.data.organization.projectV2.fields.nodes[] | select(.name== "Sprint role") | .options[] | select(.name=="%s") |.id'
    GET_LABEL_ID        = '.data.repository.issue.labels.nodes[] | select(.name == "%s")'

    GET_ISSUE_NODE_ID   = '.data.repository.issue.id'
    GET_PR_NODE_ID      = '.data.repository.pullRequest.id'
    GET_PROJECT_ITEM_ID   = '.data.addProjectV2ItemById.item.id'

    GET_ISSUE_TITLE = '.data.repository.issue.title'
    GET_PR_REF_NAME = '.data.repository.pullRequest.headRefName'
    GET_PR_COMMENTS = '.data.repository.pullRequest.body'

RoleStr: TypeAlias = Literal["Responsabile", "Amministratore", "Analista", "Verificatore", "Programmatore", "Progettista"]

ROLES: list[RoleStr] = [
    "Responsabile",
    "Amministratore",
    "Analista",
    "Verificatore",
    "Programmatore",
    "Progettista"
]

PARENT_ISSUES: dict[str, tuple[str, str, int]] = {
    "pdp":       ("GlitchHub-Team",  "GlitchHub-Team.github.io",  37,),    # Piano di Progetto
    "ndp":       ("GlitchHub-Team",  "GlitchHub-Team.github.io",  38,),    # Norme di Progetto
    "adr":       ("GlitchHub-Team",  "GlitchHub-Team.github.io",  39,),    # Analisi dei Requisiti
    "pdq":       ("GlitchHub-Team",  "GlitchHub-Team.github.io",  61,),    # Piano di Qualifica
    "gloss":     ("GlitchHub-Team",  "GlitchHub-Team.github.io", 108,),   # Glossario
    "glossario": ("GlitchHub-Team",  "GlitchHub-Team.github.io", 108,),   
    "st":        ("GlitchHub-Team",  "GlitchHub-Team.github.io", 327,),    # Specifica tecnica
}

ISSUE_BRANCH_PREFIX = "issue-"
ISSUE_BRANCH_GET_NUMBER_REGEX = r"issue-(\d+)"