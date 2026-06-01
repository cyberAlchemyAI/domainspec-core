import { useParams } from 'react-router-dom';

export default function Drafting() {
  const { cycleId } = useParams();

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', borderBottom: '1px solid #334155', paddingBottom: '0.5rem' }}>
        <h2 style={{ margin: 0, border: 'none' }}>Drafting: {cycleId}</h2>
        <div style={{ display: 'flex', gap: '1rem', fontSize: '0.9em', color: '#94A3B8' }}>
          <span>🔄 Autosave: On</span>
          <span>🔑 Edit Lease: Acquired (user_01)</span>
        </div>
      </div>

      <div className="error-banner" style={{ marginBottom: '1rem' }}>
        🔒 Project Narrative Locked by E-102
      </div>

      <div style={{ opacity: 0.6, pointerEvents: 'none' }}>
        <div style={{ border: '1px solid #334155', padding: '1rem', borderRadius: '8px', marginBottom: '1rem', backgroundColor: '#0F172A' }}>
          <h3>1. Background and Significance</h3>
          <p style={{ color: '#94A3B8' }}>[Locked]</p>
        </div>
        
        <div style={{ border: '1px solid #dc2626', padding: '1rem', borderRadius: '8px', marginBottom: '1rem', backgroundColor: '#450a0a' }}>
          <h3 style={{ color: '#fca5a5' }}>2. Approach and Methodology ⚠️ (Risk-Marked)</h3>
          <p style={{ color: '#fecaca' }}>[Locked] Note: Overridden eligibility risk propagates here.</p>
        </div>
      </div>
    </div>
  );
}
