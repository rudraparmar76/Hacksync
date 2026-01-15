import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function AuthWrapper({ children }) {
  const navigate = useNavigate();

  return (
    <div className="auth-wrapper">
      <button 
        className="back-button"
        onClick={() => navigate('/')}
      >
        ← Back to Home
      </button>
      {children}
    </div>
  );
}
