import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { SubstrateClient, type IdentityContext } from './api/SubstrateClient';
import Scout from './routes/Scout';
import Upload from './routes/Upload';
import Application from './routes/Application';
import Eligibility from './routes/Eligibility';
import Drafting from './routes/Drafting';
import Audit from './routes/Audit';
import './App.css';

// Default hardcoded identity for smoke test
const defaultIdentity: IdentityContext = {
  user_id: "demo_operator",
  applied_as: "tilth_admin",
  token_validity: true,
  is_human: false
};

const substrate = new SubstrateClient(defaultIdentity);

export default function App() {
  return (
    <BrowserRouter>
      <div className="container" style={{ flexDirection: 'row', minHeight: '100vh', padding: 0 }}>
        {/* Sidebar */}
        <aside style={{ width: '250px', backgroundColor: '#1E293B', padding: '2rem', borderRight: '1px solid #334155' }}>
          <h1 style={{ fontSize: '1.5em', color: '#F8FAFC', margin: '0 0 2rem 0' }}>Tilth OS</h1>
          <nav style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <Link to="/" style={{ color: '#94A3B8', textDecoration: 'none' }}>Scout</Link>
            <Link to="/upload" style={{ color: '#94A3B8', textDecoration: 'none' }}>Upload</Link>
            <Link to="/application/cyc_09F82A" style={{ color: '#94A3B8', textDecoration: 'none' }}>Application</Link>
            <Link to="/eligibility/cyc_09F82A" style={{ color: '#94A3B8', textDecoration: 'none' }}>Eligibility</Link>
            <Link to="/drafting/cyc_09F82A" style={{ color: '#94A3B8', textDecoration: 'none' }}>Drafting</Link>
            <Link to="/audit/cyc_09F82A" style={{ color: '#94A3B8', textDecoration: 'none' }}>Audit</Link>
          </nav>
        </aside>

        {/* Main Content */}
        <main style={{ flex: 1, padding: '2rem', textAlign: 'left' }}>
          <Routes>
            <Route path="/" element={<Scout substrate={substrate} />} />
            <Route path="/scout" element={<Scout substrate={substrate} />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/application/:cycleId" element={<Application />} />
            <Route path="/eligibility/:cycleId" element={<Eligibility />} />
            <Route path="/drafting/:cycleId" element={<Drafting />} />
            <Route path="/audit/:cycleId" element={<Audit />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
