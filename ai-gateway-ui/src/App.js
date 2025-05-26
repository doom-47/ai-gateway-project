import React, { useState, useEffect } from 'react';
import UsageDashboard from './UsageDashboard'; // Import the dashboard component
import Login from './Login'; // Import the login component
import './App.css'; // Your main CSS file

function App() {
  // State to track if the user is logged in
  const [loggedIn, setLoggedIn] = useState(false);

  // useEffect to check for existing token on component mount
  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      setLoggedIn(true); // If token exists, set loggedIn to true
    }
  }, []); // Empty dependency array means this runs once on mount

  // Callback function for successful login from Login component
  const handleLoginSuccess = () => {
    setLoggedIn(true); // Set loggedIn to true, which will render UsageDashboard
  };

  // Callback function for logout from UsageDashboard component
  const handleLogout = () => {
    localStorage.removeItem('accessToken'); // Clear the token from local storage
    setLoggedIn(false); // Set loggedIn to false, which will render Login component
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Gateway Dashboard</h1>
      </header>
      <main>
        {/* Conditional rendering: show dashboard if logged in, otherwise show login */}
        {loggedIn ? (
          <UsageDashboard onLogout={handleLogout} /> // Pass the logout handler to UsageDashboard
        ) : (
          <Login onLogin={handleLoginSuccess} /> // Pass the login success handler to Login
        )}
      </main>
    </div>
  );
}

export default App;