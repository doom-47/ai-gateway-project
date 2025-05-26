import React, { useState, useEffect, useCallback } from 'react';

// Make sure onLogout is accepted as a prop here
function UsageDashboard({ onLogout }) {
  const [usageData, setUsageData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Wrap handleLogout in useCallback
  const handleLogout = useCallback(() => {
    localStorage.removeItem('accessToken'); // Remove the token from local storage
    if (onLogout) {
      onLogout(); // Call the onLogout function passed from the parent (App.js)
    }
  }, [onLogout]); // Add onLogout to useCallback's dependency array

  useEffect(() => {
    const fetchUsage = async () => {
      const token = localStorage.getItem('accessToken'); // Get the stored token
      if (!token) {
        // If no token, set an error and stop loading
        setError('No access token found. Please log in.');
        setLoading(false);
        return;
      }

      try {
        // Make the API call to your backend with the Authorization header
        const response = await fetch('http://127.0.0.1:8000/usage/summary', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          // If response is not OK (e.g., 401, 403, 500), parse error and set it
          const errorData = await response.json();
          setError(`Failed to fetch usage data: ${response.status} - ${JSON.stringify(errorData)}`);
          // If it's an auth error, maybe log out automatically
          if (response.status === 401 || response.status === 403) {
            handleLogout(); // Log out if token is invalid/expired
          }
        } else {
          // If successful, parse data and set it to state
          const data = await response.json();
          setUsageData(data);
        }
      } catch (err) {
        // Catch any network or other unexpected errors
        setError(`An error occurred: ${err.message}`);
      } finally {
        // Always set loading to false when done
        setLoading(false);
      }
    };

    fetchUsage(); // Call the fetch function when the component mounts
  }, [onLogout, handleLogout]); // Now handleLogout is stable

  // Conditional rendering based on loading, error, or data presence
  if (loading) {
    return <div>Loading usage data...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!usageData) {
    return <div>No usage data available.</div>;
  }

  // Render the dashboard if data is available
  return (
    <div>
      {/* Logout Button */}
      <button onClick={handleLogout} style={{ float: 'right', margin: '10px' }}>Logout</button>
      <h2>Usage Summary</h2>
      <p>Total Requests: {usageData.total_requests}</p>
      <p>Total Input Tokens: {usageData.total_input_tokens}</p>
      <p>Total Output Tokens: {usageData.total_output_tokens}</p>
      <p>Estimated Total Cost (USD): {usageData.estimated_total_cost_usd}</p>

      <h3>Model Usage</h3>
      {/* Map through model_usage object to display details for each model */}
      {Object.keys(usageData.model_usage).map(model => (
        <div key={model}>
          <h4>{model.toUpperCase()}</h4>
          <p>Input Tokens: {usageData.model_usage[model].input_tokens}</p>
          <p>Output Tokens: {usageData.model_usage[model].output_tokens}</p>
          <p>Requests: {usageData.model_usage[model].requests}</p>
        </div>
      ))}
    </div>
  );
}

export default UsageDashboard;