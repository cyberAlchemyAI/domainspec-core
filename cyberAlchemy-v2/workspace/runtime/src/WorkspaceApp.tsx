import EssaysApp from "@cyberalchemy/essays-runtime";
import type { EssaysSavedDraftObservation, EssaysStagedBuffer } from "@cyberalchemy/essays-runtime/markdown";
import type { EssayWorkspace } from "@cyberalchemy/essays-runtime/model";
import "@cyberalchemy/essays-runtime/styles.css";
import { useCallback, useEffect, useMemo, useState, type ReactNode } from "react";
import { WorkspaceRuntime } from "./domain/runtime";
import { filterWorkspaceRecords, toWorkspaceViewModel, WORKSPACE_COLLECTIONS, type WorkspaceCollection, type WorkspaceRecord } from "./domain/workspace";
import { AgentDock } from "./features/agents/AgentDock";
import { OntologyCanvas } from "./features/ontology/OntologyCanvas";

const COLLECTION_LABELS: Record<WorkspaceCollection, string> = {
  definitions: "Definitions",
  products: "Products",
  projects: "Projects",
  ontologies: "Ontologies",
};

type Surface = "explore" | "ontology" | "essays";

function projectFromHash(hash: string): string | null {
  const match = /^#\/projects\/(.+)$/.exec(hash);
  return match ? decodeURIComponent(match[1]) : null;
}

function surfaceFromHash(hash: string): Surface {
  if (hash === "#/ontology") return "ontology";
  return hash === "#/essays" || projectFromHash(hash) === "CA2-PROJECT-ESSAYS" ? "essays" : "explore";
}

function AppIcon({ name }: { name: Surface | "mark" }) {
  if (name === "mark") return <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2 21 7v10l-9 5-9-5V7l9-5Z" /><path d="m8 14 4-7 4 7M9.5 12h5" /></svg>;
  if (name === "essays") return <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3h9l3 3v15H6V3Z" /><path d="M9 9h6M9 13h6M9 17h4M15 3v4h4" /></svg>;
  if (name === "ontology") return <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="5" r="2.5" /><circle cx="5" cy="17" r="2.5" /><circle cx="19" cy="17" r="2.5" /><path d="m10.7 7.2-4.4 7.6m7-7.6 4.4 7.6M7.5 17h9" /></svg>;
  return <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="7" cy="7" r="3" /><circle cx="17" cy="7" r="3" /><circle cx="12" cy="17" r="3" /><path d="m9.5 8.7 1.4 5.3m3.6-5.3-1.4 5.3M10 7h4" /></svg>;
}

function RailButton({ active, label, icon, onClick }: { active: boolean; label: string; icon: Surface; onClick: () => void }) {
  return (
    <button type="button" className={active ? "rail-action active" : "rail-action"} aria-label={label} aria-current={active ? "page" : undefined} onClick={onClick}>
      <AppIcon name={icon} />
      <span className="rail-tooltip" role="tooltip">{label}</span>
    </button>
  );
}

function RecordDetail({ record, onOpenEssays }: { record: WorkspaceRecord; onOpenEssays: () => void }) {
  const isEssays = record.collection === "projects" && record.recordId === "CA2-PROJECT-ESSAYS";
  return (
    <article className="record-detail" aria-labelledby="record-title">
      <div className="detail-heading">
        <div><p className="record-kind">{COLLECTION_LABELS[record.collection].slice(0, -1)}</p><h2 id="record-title">{record.label}</h2></div>
        <span className={`status status-${record.status.replaceAll("_", "-")}`}>{record.status}</span>
      </div>
      <p className="record-id">{record.recordId}</p>
      <p className="meaning">{record.meaning}</p>
      <dl className="detail-grid">
        <div><dt>Owner route</dt><dd>{record.ownerRoute}</dd></div>
        <div><dt>Boundary</dt><dd>{record.boundary}</dd></div>
        <div className="wide"><dt>Claim ceiling</dt><dd>{record.claimCeiling}</dd></div>
        <div className="wide"><dt>Provenance</dt><dd><ul>{record.sourceRefs.map((ref) => <li key={ref}>{ref}</li>)}</ul></dd></div>
      </dl>
      {isEssays && <button className="project-entry" type="button" onClick={onOpenEssays}><span>Open owned capability</span><strong>Essays <span aria-hidden="true">→</span></strong></button>}
    </article>
  );
}

function ExploreSurface({ onOpenEssays }: { onOpenEssays: () => void }) {
  const runtime = useMemo(() => new WorkspaceRuntime(), []);
  const snapshot = runtime.inspectWorkspace();
  const view = useMemo(() => toWorkspaceViewModel(snapshot), [snapshot]);
  const [collection, setCollection] = useState<WorkspaceCollection>("projects");
  const [query, setQuery] = useState("");
  const [selectedId, setSelectedId] = useState("CA2-PROJECT-ESSAYS");
  const records = filterWorkspaceRecords(view.collections[collection], query);
  const selected = view.collections[collection].find((item) => item.recordId === selectedId) ?? records[0] ?? view.collections[collection][0];

  const chooseCollection = (next: WorkspaceCollection) => {
    setCollection(next);
    setQuery("");
    setSelectedId(view.collections[next][0]?.recordId ?? "");
    window.history.replaceState(null, "", `#/collections/${next}`);
  };

  return (
    <main className="workspace-main">
      <header className="surface-header">
        <div><p className="eyebrow">Semantic read plane</p><h1>Explore the system.</h1></div>
        <div className="epoch-card" aria-label="Workspace source epoch"><span>Source epoch</span><code>{snapshot.sourceEpoch.slice(0, 12)}</code><small>generated · read-only</small></div>
      </header>
      <div className="collection-tabs" role="tablist" aria-label="Workspace collections">
        {WORKSPACE_COLLECTIONS.map((item) => <button key={item} role="tab" aria-selected={collection === item} className={collection === item ? "active" : ""} onClick={() => chooseCollection(item)}>{COLLECTION_LABELS[item]} <span>{view.collections[item].length}</span></button>)}
      </div>
      <section className="explorer" aria-label={`${COLLECTION_LABELS[collection]} explorer`}>
        <div className="record-browser">
          <div className="browser-heading"><div><p className="section-number">{String(WORKSPACE_COLLECTIONS.indexOf(collection) + 1).padStart(2, "0")}</p><h2>{COLLECTION_LABELS[collection]}</h2></div><span>{view.collections[collection].length} records</span></div>
          <label className="search-field"><span className="sr-only">Search {COLLECTION_LABELS[collection]}</span><span aria-hidden="true">⌕</span><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder={`Search ${collection}…`} /></label>
          <div className="record-list" role="list">
            {records.map((record) => <button key={record.recordId} role="listitem" className={selected?.recordId === record.recordId ? "selected" : ""} onClick={() => setSelectedId(record.recordId)}><span className="record-list-main"><strong>{record.label}</strong><small>{record.recordId}</small></span><span className="record-arrow" aria-hidden="true">→</span></button>)}
            {records.length === 0 && <p className="empty-result">No records match “{query}”.</p>}
          </div>
        </div>
        {selected && <RecordDetail record={selected} onOpenEssays={onOpenEssays} />}
      </section>
      <footer className="workspace-footer"><p><strong>Projection, not authority.</strong> Visibility does not prove admission, conformance, correctness, or product value.</p><p>Snapshot <code>{snapshot.snapshotId.slice(0, 16)}</code></p></footer>
    </main>
  );
}

function SurfaceFrame({ children }: { children: ReactNode }) {
  return <section className="surface-frame">{children}</section>;
}

export default function WorkspaceApp() {
  const [surface, setSurface] = useState<Surface>(() => surfaceFromHash(window.location.hash));
  const [essayWorkspace, setEssayWorkspace] = useState<EssayWorkspace | null>(null);
  const [stagedBuffer, setStagedBuffer] = useState<EssaysStagedBuffer | null>(null);
  const [savedDraftObservation, setSavedDraftObservation] = useState<EssaysSavedDraftObservation | null>(null);

  useEffect(() => {
    const update = () => setSurface(surfaceFromHash(window.location.hash));
    window.addEventListener("hashchange", update);
    return () => window.removeEventListener("hashchange", update);
  }, []);

  const navigate = useCallback((next: Surface) => {
    const hash = next === "essays" ? "#/essays" : next === "ontology" ? "#/ontology" : "#/collections/projects";
    window.history.replaceState(null, "", hash);
    setSurface(next);
  }, []);
  const receiveEssayWorkspace = useCallback((workspace: EssayWorkspace | null) => setEssayWorkspace(workspace), []);

  return (
    <div className="workspace-shell">
      <aside className="app-rail" aria-label="Application navigation">
        <div className="brand-mark" aria-label="CyberAlchemy Workspace"><AppIcon name="mark" /></div>
        <nav aria-label="Workspace surfaces">
          <RailButton active={surface === "explore"} label="Explore workspace" icon="explore" onClick={() => navigate("explore")} />
          <RailButton active={surface === "ontology"} label="Open Ontology" icon="ontology" onClick={() => navigate("ontology")} />
          <RailButton active={surface === "essays"} label="Open Essays" icon="essays" onClick={() => navigate("essays")} />
        </nav>
        <div className="local-indicator" title="Local candidate runtime"><span /><span className="sr-only">Local candidate runtime</span></div>
      </aside>
      <SurfaceFrame>
        {surface === "explore" ? <ExploreSurface onOpenEssays={() => navigate("essays")} /> : surface === "ontology" ? <OntologyCanvas /> : (
          <div className="essays-composition">
            <section className="essays-owned-plane" aria-label="Essays project capability">
              <div className="ownership-strip"><span>Essays-owned action plane</span><strong>Workspace composes · Essays decides</strong></div>
              <EssaysApp
                embedded
                onWorkspaceChange={receiveEssayWorkspace}
                stagedBuffer={stagedBuffer}
                onSavedDraftObservation={setSavedDraftObservation}
              />
            </section>
            <AgentDock
              essayWorkspace={essayWorkspace}
              savedDraftObservation={savedDraftObservation}
              onStageBuffer={setStagedBuffer}
            />
          </div>
        )}
      </SurfaceFrame>
    </div>
  );
}
