import { useState } from 'react';
import FileUpload from './components/FileUpload';
import AdminDashboard from './components/AdminDashboard';

function App() {
  const [view, setView] = useState('client');

  const buttonStyle = (active) => ({
    padding: '10px 20px',
    cursor: 'pointer',
    backgroundColor: active ? '#2563eb' : '#e2e8f0',
    color: active ? '#ffffff' : '#000000',
    border: 'none',
    borderRadius: '6px',
    fontWeight: 700
  });

  return (
    <div style={{ textAlign: 'center', fontFamily: 'sans-serif', padding: '20px' }}>
      <div style={{ marginBottom: '30px', display: 'flex', justifyContent: 'center', gap: '15px' }}>
        <button onClick={() => setView('client')} style={buttonStyle(view === 'client')}>
          Client Upload Portal
        </button>
        <button onClick={() => setView('admin')} style={buttonStyle(view === 'admin')}>
          Admin Dashboard
        </button>
      </div>

      {view === 'client' ? (
        <div>
          <h1>TrustGate Client Portal</h1>
          <p>Please upload your identity documents for secure verification.</p>
          <FileUpload />
        </div>
      ) : (
        <AdminDashboard />
      )}
    </div>
  );
}

export default App;