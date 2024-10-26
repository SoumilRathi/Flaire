import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Reset = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Clear all items from localStorage
    localStorage.clear();
    console.log('Local storage has been cleared.');

    // Redirect to the home page after clearing
    navigate('/');
  }, [navigate]);

  return (
    <div>
      <h1>Resetting...</h1>
      <p>Clearing local storage and redirecting to home page.</p>
    </div>
  );
};

export default Reset;
