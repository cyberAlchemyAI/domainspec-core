import { useParams } from 'react-router-dom';

export default function Audit() {
  const { cycleId } = useParams();

  return (
    <div className="card">
      <h2>Audit Trail: {cycleId}</h2>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1rem' }}>
        
        <div style={{ padding: '1rem', border: '1px solid #334155', borderRadius: '8px', borderLeft: '4px solid #ef4444' }}>
          <h3 style={{ color: '#F1F5F9', marginTop: 0 }}>Logician Gate Halt</h3>
          <p style={{ color: '#94A3B8', margin: 0 }}>Process halted at E-102 due to missing UEI registration.</p>
        </div>

        <div style={{ padding: '1rem', border: '1px solid #334155', borderRadius: '8px', borderLeft: '4px solid #ef4444' }}>
          <h3 style={{ color: '#F1F5F9', marginTop: 0 }}>Budget Validation Failure</h3>
          <p style={{ color: '#94A3B8', margin: 0 }}>Total proposed budget exceeds NOFO ceiling constraint.</p>
        </div>

        <div style={{ padding: '1rem', border: '1px solid #334155', borderRadius: '8px', borderLeft: '4px solid #eab308' }}>
          <h3 style={{ color: '#F1F5F9', marginTop: 0 }}>Signature State: Unsigned Changes Pending</h3>
          <p style={{ color: '#94A3B8', margin: 0 }}>There are 3 unverified events pending cryptographic signature.</p>
        </div>

        <div style={{ padding: '1rem', border: '1px solid #334155', borderRadius: '8px', borderLeft: '4px solid #3b82f6' }}>
          <h3 style={{ color: '#F1F5F9', marginTop: 0 }}>Posture Change Event</h3>
          <p style={{ color: '#94A3B8', margin: 0 }}>System posture elevated to SPLIT_CONTEXT_HYBRID prior to final narrative synthesis.</p>
        </div>

      </div>
    </div>
  );
}
