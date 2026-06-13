import { SubstrateClient } from '../api/SubstrateClient';

export default function Scribe({ onBack }: { substrate: SubstrateClient, onBack?: () => void }) {
  // Scribe is the drafting workbench area.
  // We use the substrate client to eventually load drafting components.
  
  return (
    <div className="card">
      {onBack && (
        <button type="button" onClick={onBack} style={{ marginBottom: '1rem', cursor: 'pointer' }}>
          ← Back to Home
        </button>
      )}
      <h2>Scribe Drafting Workbench</h2>
      <p style={{ color: '#94A3B8' }}>Develop source-grounded drafts and support documents.</p>
      
      <div style={{ marginTop: '2rem', padding: '1rem', border: '1px dashed #334155', borderRadius: '8px' }}>
        <p>Section-by-section drafting components will appear here once connected.</p>
      </div>
    </div>
  );
}
