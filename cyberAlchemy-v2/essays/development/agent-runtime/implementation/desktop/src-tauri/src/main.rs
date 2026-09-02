use essays_agent_runtime::{
    Command, Receipt, Runtime, SqliteStore, WorkspaceSnapshot, security::local_process_principal,
};
use serde::Serialize;
use std::path::PathBuf;
use tauri::{Manager, State};

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
struct PrincipalEvidence {
    principal_subject: String,
    client_id: String,
    evidence_kind: &'static str,
    verified_human_identity: bool,
}

#[tauri::command]
fn principal_evidence() -> PrincipalEvidence {
    let principal = local_process_principal("essays-tauri");
    PrincipalEvidence {
        principal_subject: principal.subject().to_string(),
        client_id: principal.client_id().to_string(),
        evidence_kind: "local-process",
        verified_human_identity: false,
    }
}

#[tauri::command]
fn execute(command: Command, runtime: State<'_, Runtime>) -> Result<Receipt, String> {
    let principal = local_process_principal("essays-tauri");
    runtime
        .execute(&command, &principal)
        .map_err(|error| error.to_string())
}

#[tauri::command]
fn snapshot(
    workspace_id: String,
    cursor: Option<i64>,
    runtime: State<'_, Runtime>,
) -> Result<Option<WorkspaceSnapshot>, String> {
    runtime
        .snapshot(&workspace_id, cursor)
        .map_err(|error| error.to_string())
}

fn main() {
    let builder = tauri::Builder::default();
    #[cfg(feature = "wdio")]
    let builder = builder
        .plugin(tauri_plugin_wdio::init())
        .plugin(tauri_plugin_wdio_webdriver::init());

    #[cfg(feature = "wdio")]
    let context = tauri::generate_context!(capabilities = ["wdio/capabilities/wdio-smoke.json"]);
    #[cfg(not(feature = "wdio"))]
    let context = tauri::generate_context!();

    builder
        .setup(|app| {
            let data_dir = app.path().app_data_dir()?;
            let database = std::env::var_os("ESSAYS_DATABASE")
                .map(PathBuf::from)
                .unwrap_or_else(|| data_dir.join("essays.db"));
            if let Some(parent) = database.parent() {
                std::fs::create_dir_all(parent)?;
            }
            let store =
                SqliteStore::open(database).map_err(|error| anyhow_for_tauri(error.to_string()))?;
            app.manage(Runtime::new(store));
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            execute,
            snapshot,
            principal_evidence
        ])
        .run(context)
        .expect("run Essays desktop shell");
}

fn anyhow_for_tauri(message: String) -> Box<dyn std::error::Error> {
    Box::new(std::io::Error::other(message))
}

#[cfg(test)]
mod tests {
    use super::principal_evidence;

    #[test]
    fn principal_evidence_keeps_subject_and_client_identity_distinct() {
        let evidence = principal_evidence();
        assert!(evidence.principal_subject.starts_with("unix:"));
        assert_eq!(evidence.client_id, "essays-tauri");
        assert_eq!(evidence.evidence_kind, "local-process");
        assert!(!evidence.verified_human_identity);
        assert_ne!(evidence.principal_subject, evidence.client_id);
    }
}
