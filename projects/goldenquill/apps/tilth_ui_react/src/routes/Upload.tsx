export default function Upload() {
  return (
    <div className="card">
      <h2>Upload Intake</h2>
      <div className="error-banner" style={{ backgroundColor: '#78350f', borderColor: '#d97706', color: '#fef3c7', marginBottom: '1rem' }}>
        <strong>ℹ️ Important:</strong> RFA / NOFO Document MUST be the first upload.
      </div>
      <p style={{ color: '#94A3B8' }}>Select your application guidelines before adding supplemental documentation.</p>
    </div>
  );
}
