import { useState } from 'react';

export default function FileUpload() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    // Grab the first file the user selects
    setFile(e.target.files[0]);
    // Reset previous errors and results when a new file is picked
    setError(null);
    setResult(null);
  };

  const handleUpload = async (e) => {
    e.preventDefault(); // Prevent the page from refreshing when the form submits
    
    if (!file) {
      setError("Please select a file first.");
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/upload', {
        method: 'POST',
        body: formData
        // Notice: NO headers are set here. The browser does it for FormData automatically!
      });

      if (!response.ok) {
        // Try to read the error message from the FastAPI backend
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Server error: ${response.status}`);
      }

      // Parse the successful response
      const data = await response.json();
      setResult(data);

    } catch (err) {
      // Catch network errors (like CORS) or our custom thrown errors
      setError(err.message || "Failed to upload document.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '550px', margin: '40px auto', padding: '25px', border: '1px solid #e2e8f0', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
      <h2 style={{ color: '#1e293b', marginTop: 0 }}>Secure Document Upload</h2>
      
      <form onSubmit={handleUpload} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
        <input 
          type="file" 
          onChange={handleFileChange} 
          accept=".pdf,.png,.jpg,.jpeg" 
          style={{ padding: '10px', border: '2px dashed #cbd5e1', borderRadius: '8px', cursor: 'pointer' }}
        />
        
        <button 
          type="submit" 
          disabled={!file || loading} 
          style={{ 
            padding: '12px', 
            backgroundColor: loading || !file ? '#94a3b8' : '#2563eb', 
            color: '#fff', 
            border: 'none', 
            borderRadius: '8px',
            cursor: loading || !file ? 'not-allowed' : 'pointer',
            fontWeight: 'bold',
            fontSize: '16px'
          }}
        >
          {loading ? "Processing Securely..." : "Upload & Verify"}
        </button>
      </form>

      {/* Error Message Display */}
      {error && (
        <div style={{ color: '#b91c1c', backgroundColor: '#fef2f2', padding: '12px', marginTop: '20px', borderRadius: '8px', border: '1px solid #f87171' }}>
          <strong>Error: </strong>{error}
        </div>
      )}

      {/* Success Result Display */}
      {result && (
        <div style={{ marginTop: '25px', padding: '20px', backgroundColor: '#f8fafc', borderRadius: '8px', textAlign: 'left', border: '1px solid #e2e8f0' }}>
          <h3 style={{ marginTop: 0, color: '#0f172a' }}>Verification Complete ✅</h3>
          <p style={{ margin: '5px 0' }}><strong>Status:</strong> {result.status}</p>
          <p style={{ margin: '5px 0' }}><strong>Saved As:</strong> {result.saved_as}</p>
          
          <div style={{ marginTop: '15px', backgroundColor: '#1e293b', color: '#10b981', padding: '15px', borderRadius: '8px', overflowX: 'auto' }}>
            <pre style={{ margin: 0, fontSize: '14px', fontFamily: 'monospace' }}>
              {JSON.stringify(result.document_analysis, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}