import React from 'react'
import FileUpload from './components/FileUpload';

function App() {
  return (
    <div style={{ textAlign: 'center', fontFamily: 'sans-serif' }}>
      <h1>TrustGate Client Portal</h1>
      <p>Please upload your identity documents for secure verification.</p>
      <FileUpload />
    </div>
  );
}

export default App;