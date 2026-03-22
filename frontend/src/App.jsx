import { useState } from 'react';
import FileUpload from './components/FileUpload';
import AdminDashboard from './components/AdminDashboard';

function App() {
  const [view, setView] = useState('client'); // 'client' or 'admin'

  return (
    <div style={{ textAlign: 'center', fontFamily: 'sans-serif', padding: '20px' }}>
      
      {/* Navigation Bar */}
      <div style={{ marginBottom: '30px', display: 'flex', justifyContent: 'center', gap: '15px' }}>
        <button 
          onClick={() => setView('client')}
          style={{ padding: '10px 20px', cursor: 'pointer', backgroundColor: view === 'client' ? '#2563eb' : '#e2e8f0', color: view === 'client' ? 'white' : 'black', border: 'none', borderRadius: '6px', fontWeight: 'bold' }}
        >
          Client Upload Portal
        </button>
        <button 
          onClick={() => setView('admin')}
          style={{ padding: '10px 20px', cursor: 'pointer', backgroundColor: view === 'admin' ? '#2563eb' : '#e2e8f0', color: view === 'admin' ? 'white' : 'black', border: 'none', borderRadius: '6px', fontWeight: 'bold' }}
        >
          Admin Dashboard
        </button>
      </div>

      {/* Render the selected view */}
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