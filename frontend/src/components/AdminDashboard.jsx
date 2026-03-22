import { useState, useEffect } from 'react';

export default function AdminDashboard() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // useEffect runs automatically when the component loads
  useEffect(() => {
    fetchRecords();
  }, []);

  const fetchRecords = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/documents');
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }
      const data = await response.json();
      
      // Reverse the array so the newest uploads show at the top of the table
      setRecords(data.data.reverse() || []);
    } catch (err) {
      setError(err.message || "Failed to fetch records.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <h3 style={{ textAlign: 'center' }}>Loading Dashboard...</h3>;
  if (error) return <div style={{ color: 'red', textAlign: 'center' }}>Error: {error}</div>;

  return (
    <div style={{ maxWidth: '1000px', margin: '40px auto', padding: '20px', fontFamily: 'sans-serif' }}>
      <h2 style={{ color: '#1e293b' }}>Compliance Admin Dashboard</h2>
      <p style={{ color: '#64748b', marginBottom: '20px' }}>Review all client onboarding documents.</p>
      
      <div style={{ overflowX: 'auto', border: '1px solid #e2e8f0', borderRadius: '8px' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
          <thead style={{ backgroundColor: '#f8fafc', borderBottom: '2px solid #e2e8f0' }}>
            <tr>
              <th style={{ padding: '12px 16px', color: '#334155' }}>Date/Time</th>
              <th style={{ padding: '12px 16px', color: '#334155' }}>Original File</th>
              <th style={{ padding: '12px 16px', color: '#334155' }}>Extracted PAN</th>
              <th style={{ padding: '12px 16px', color: '#334155' }}>PAN Valid?</th>
            </tr>
          </thead>
          <tbody>
            {records.length === 0 ? (
              <tr>
                <td colSpan="4" style={{ padding: '20px', textAlign: 'center', color: '#94a3b8' }}>No documents processed yet.</td>
              </tr>
            ) : (
              records.map((record, index) => {
                const panData = record.document_analysis?.extracted_data?.pan_data || {};
                const date = new Date(record.timestamp).toLocaleString();
                
                return (
                  <tr key={index} style={{ borderBottom: '1px solid #e2e8f0', backgroundColor: index % 2 === 0 ? '#ffffff' : '#f8fafc' }}>
                    <td style={{ padding: '12px 16px', fontSize: '14px', color: '#475569' }}>{date}</td>
                    <td style={{ padding: '12px 16px', fontSize: '14px', fontWeight: '500' }}>{record.original_filename}</td>
                    <td style={{ padding: '12px 16px', fontFamily: 'monospace', color: panData.number ? '#0f172a' : '#94a3b8' }}>
                      {panData.number || "Not Found"}
                    </td>
                    <td style={{ padding: '12px 16px' }}>
                      {panData.is_valid ? (
                        <span style={{ backgroundColor: '#dcfce7', color: '#166534', padding: '4px 8px', borderRadius: '9999px', fontSize: '12px', fontWeight: 'bold' }}>Valid</span>
                      ) : (
                        <span style={{ backgroundColor: '#fee2e2', color: '#991b1b', padding: '4px 8px', borderRadius: '9999px', fontSize: '12px', fontWeight: 'bold' }}>Invalid/None</span>
                      )}
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}