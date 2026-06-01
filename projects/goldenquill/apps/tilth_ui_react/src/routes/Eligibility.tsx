import { useParams } from 'react-router-dom';

export default function Eligibility() {
  const { cycleId } = useParams();

  return (
    <div className="card">
      <h2>Eligibility & Compliance: {cycleId}</h2>
      
      <div className="error-banner" style={{ marginBottom: '1rem' }}>
        ⛔ E-102: FAIL_CLOSED
        <span style={{ fontSize: '0.8em', backgroundColor: 'black', padding: '0.2rem 0.5rem', borderRadius: '4px' }}>DO NOT DRAFT</span>
      </div>

      <div style={{ padding: '1rem', border: '1px solid #334155', borderRadius: '8px', marginBottom: '1rem' }}>
        <h3 style={{ color: '#F1F5F9' }}>Gate Status</h3>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          <li style={{ color: '#DC2626', marginBottom: '0.5rem' }}>❌ <strong>E-102:</strong> Required Entity Registration missing.</li>
          <li style={{ color: '#94A3B8', marginBottom: '0.5rem' }}>⏸️ <strong>E-103:</strong> UNTESTED_DUE_TO_BLOCK</li>
          <li style={{ color: '#94A3B8', marginBottom: '0.5rem' }}>⏸️ <strong>E-104:</strong> UNTESTED_DUE_TO_BLOCK</li>
        </ul>
      </div>

      <div style={{ padding: '1rem', border: '1px solid #334155', borderRadius: '8px', marginBottom: '1rem' }}>
        <h3 style={{ color: '#F1F5F9' }}>Remediation</h3>
        <p style={{ color: '#94A3B8' }}>Supply active SAM.gov UEI registration evidence matching the target applicant.</p>
      </div>

      <div style={{ padding: '1rem', backgroundColor: '#450a0a', border: '1px solid #dc2626', borderRadius: '8px' }}>
        <h3 style={{ color: '#fca5a5', marginTop: 0 }}>⚠️ Risky Signed Override</h3>
        <p style={{ color: '#fecaca', fontSize: '0.9em' }}>
          An operator has forced an override on E-102. Scribe access is unlocked, but the final package will be flagged.
        </p>
      </div>
    </div>
  );
}
