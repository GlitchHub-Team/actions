# actions
Repository che contiene tutte le automazioni per GitHub Actions usate dal gruppo GlitchHub-Team.

## issue-action.yml
Workflow chiamati per una migliore gestione delle issue. Permette di associare i campi di Project "Sprint" e "Sprint Role"

### Parametri
- `issue-event`: può essere `"open"` se è stata aperta l'issue oppure `"label"` se sono cambiati i suoi label
- `project`: Il GitHub Project al quale aggiungere l'issue. Dovrebbe essere `"GlitchHub-Team/2"`, visto che usiamo un unico Project.
