import { useEffect, useMemo, useState } from "react";
import { WorkspaceRuntime } from "./domain/runtime";
import { filterWorkspaceRecords, toWorkspaceViewModel, WORKSPACE_COLLECTIONS, type WorkspaceCollection, type WorkspaceRecord } from "./domain/workspace";

const COLLECTION_LABELS: Record<WorkspaceCollection, string> = {
  definitions: "Definitions",
  products: "Products",
  projects: "Projects",
  ontologies: "Ontologies",
};

function projectFromHash(hash: string): string | null {
  const match = /^#\/projects\/(.+)$/.exec(hash);
  return match ? decodeURIComponent(match[1]) : null;
}

function RecordDetail({ record, projectSurface }: { record: WorkspaceRecord; projectSurface: boolean }) {
  return (
    <article className="record-detail" aria-labelledby="record-title">
      {projectSurface && <p className="surface-marker">Project surface <span>separately owned</span></p>}
      <div className="detail-heading">
        <div>
          <p className="record-kind">{COLLECTION_LABELS[record.collection].slice(0, -1)}</p>
          <h2 id="record-title">{record.label}</h2>
        </div>
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

      {record.collection === "projects" && !projectSurface && record.projectEntryRef && (
        <a className="project-entry" href={record.projectEntryRef}>
          <span>Open project</span>
          <strong>{record.label} <span aria-hidden="true">↗</span></strong>
        </a>
      )}
      {projectSurface && (
        <div className="project-boundary-note">
          <strong>This is a navigation surface, not an invocation.</strong>
          <p>The Workspace can describe and locate this Project. It cannot edit, activate, accept, or take ownership of it.</p>
        </div>
      )}
    </article>
  );
}

export default function App() {
  const runtime = useMemo(() => new WorkspaceRuntime(), []);
  const snapshot = runtime.inspectWorkspace();
  const view = useMemo(() => toWorkspaceViewModel(snapshot), [snapshot]);
  const [hash, setHash] = useState(window.location.hash);
  const initialProject = projectFromHash(window.location.hash);
  const [collection, setCollection] = useState<WorkspaceCollection>(initialProject ? "projects" : "products");
  const [query, setQuery] = useState("");
  const [selectedId, setSelectedId] = useState(initialProject ?? "CA2-CAP-INSPECT-CYBERALCHEMY-WORKSPACE");

  useEffect(() => {
    const update = () => {
      setHash(window.location.hash);
      const project = projectFromHash(window.location.hash);
      if (project) {
        setCollection("projects");
        setSelectedId(project);
        setQuery("");
      }
    };
    window.addEventListener("hashchange", update);
    return () => window.removeEventListener("hashchange", update);
  }, []);

  const records = filterWorkspaceRecords(view.collections[collection], query);
  const selected = view.collections[collection].find((item) => item.recordId === selectedId)
    ?? records[0]
    ?? view.collections[collection][0];
  const projectSurface = projectFromHash(hash) === selected?.recordId;

  const chooseCollection = (next: WorkspaceCollection) => {
    setCollection(next);
    setQuery("");
    setSelectedId(view.collections[next][0]?.recordId ?? "");
    window.history.replaceState(null, "", `#/collections/${next}`);
    setHash(window.location.hash);
  };

  return (
    <div className="workspace-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <span className="sigil" aria-hidden="true">CA</span>
          <div><p>CyberAlchemy</p><strong>Workspace</strong></div>
        </div>
        <nav aria-label="Workspace collections">
          <p className="nav-label">Explore meaning</p>
          {WORKSPACE_COLLECTIONS.map((item, index) => (
            <button key={item} className={collection === item ? "active" : ""} onClick={() => chooseCollection(item)} aria-current={collection === item ? "page" : undefined}>
              <span className="nav-index">0{index + 1}</span>
              <span>{COLLECTION_LABELS[item]}</span>
              <span className="count">{view.collections[item].length}</span>
            </button>
          ))}
        </nav>
        <div className="authority-note">
          <span className="read-dot" aria-hidden="true" />
          <div><strong>Inspect only</strong><p>No source or authority mutation.</p></div>
        </div>
      </aside>

      <main className="workspace-main">
        <header className="hero">
          <div>
            <p className="eyebrow">A source-owned semantic map</p>
            <h1>Understand the system<br />before changing it.</h1>
          </div>
          <div className="epoch-card" aria-label="Workspace source epoch">
            <span>Source epoch</span>
            <code>{snapshot.sourceEpoch.slice(0, 12)}</code>
            <small>generated · read-only</small>
          </div>
        </header>

        <section className="explorer" aria-label={`${COLLECTION_LABELS[collection]} explorer`}>
          <div className="record-browser">
            <div className="browser-heading">
              <div><p className="section-number">{String(WORKSPACE_COLLECTIONS.indexOf(collection) + 1).padStart(2, "0")}</p><h2>{COLLECTION_LABELS[collection]}</h2></div>
              <span>{view.collections[collection].length} records</span>
            </div>
            <label className="search-field">
              <span className="sr-only">Search {COLLECTION_LABELS[collection]}</span>
              <span aria-hidden="true">⌕</span>
              <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder={`Search ${collection}…`} />
            </label>
            <div className="record-list" role="list">
              {records.map((record) => (
                <button key={record.recordId} role="listitem" className={selected?.recordId === record.recordId ? "selected" : ""} onClick={() => { setSelectedId(record.recordId); window.history.replaceState(null, "", `#/collections/${collection}/${encodeURIComponent(record.recordId)}`); setHash(window.location.hash); }}>
                  <span className="record-list-main"><strong>{record.label}</strong><small>{record.recordId}</small></span>
                  <span className="record-arrow" aria-hidden="true">→</span>
                </button>
              ))}
              {records.length === 0 && <p className="empty-result">No records match “{query}”.</p>}
            </div>
          </div>
          {selected && <RecordDetail record={selected} projectSurface={projectSurface} />}
        </section>

        <footer className="workspace-footer">
          <p><strong>Projection, not authority.</strong> Visibility does not prove admission, conformance, correctness, or product value.</p>
          <p>Snapshot <code>{snapshot.snapshotId.slice(0, 16)}</code></p>
        </footer>
      </main>
    </div>
  );
}
