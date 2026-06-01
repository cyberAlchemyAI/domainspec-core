import { useParams, Link } from 'react-router-dom';
import DEMO_DATA from '../data/mock/DEMO_DATA.json';

export default function Application() {
  const { cycleId } = useParams();
  const modules = DEMO_DATA.module_map;

  return (
    <div className="card">
      <h2>Project Application: {cycleId}</h2>
      <p style={{ color: '#94A3B8' }}>Guides Project Narrative section-by-section.</p>
      
      <div style={{ marginTop: '1rem' }}>
        {modules.map(mod => (
          <div key={mod.section_id} style={{ padding: '1rem', border: '1px solid #334155', borderRadius: '8px', marginBottom: '1rem', backgroundColor: '#0F172A' }}>
            <h3 style={{ color: '#F1F5F9', marginTop: 0 }}>{mod.title}</h3>
            <ul style={{ color: '#94A3B8', listStyle: 'none', padding: 0 }}>
              <li><strong>Word Limit:</strong> {mod.word_limit}</li>
              <li><strong>Rubric Weight:</strong> {(mod.rubric_weight * 100).toFixed(0)}%</li>
              <li><strong>Sensitivity:</strong> <span style={{ color: '#FCD34D' }}>{mod.sensitivity}</span></li>
              <li><strong>Recommended Posture:</strong> <span style={{ color: '#A7F3D0' }}>{mod.recommended_posture}</span></li>
            </ul>
            <div style={{ marginTop: '0.5rem' }}>
              <strong style={{ color: '#E2E8F0' }}>Required Evidence:</strong>
              <ul style={{ color: '#94A3B8', paddingLeft: '1.5rem', marginTop: '0.25rem' }}>
                {mod.required_evidence.map(ev => <li key={ev}>{ev}</li>)}
              </ul>
              <div style={{ marginTop: '1rem' }}>
                <Link to="/upload" style={{ color: '#38bdf8', textDecoration: 'none' }}>
                  Missing Evidence? Return to Upload ↗
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
