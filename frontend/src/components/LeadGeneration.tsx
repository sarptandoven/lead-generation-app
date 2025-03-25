import React, { useState } from 'react';
import styled from 'styled-components';
import LoadingSpinner from './LoadingSpinner';
import { checkAuth } from '../services/authService';

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
`;

const Button = styled.button`
  background-color: #3498db;
  color: white;
  padding: 1rem 2rem;
  border: none;
  border-radius: 4px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.2s;

  &:hover {
    background-color: #2980b9;
  }

  &:disabled {
    background-color: #bdc3c7;
    cursor: not-allowed;
  }
`;

const ErrorMessage = styled.div`
  color: #e74c3c;
  padding: 1rem;
  margin-top: 1rem;
  border: 1px solid #e74c3c;
  border-radius: 4px;
  background-color: #fadbd8;
`;

const LeadGeneration: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerateLeads = async () => {
    setIsLoading(true);
    setError(null);

    // Random delay between 3-10 seconds
    const delay = Math.floor(Math.random() * (10000 - 3000 + 1) + 3000);

    try {
      // Wait for the random delay
      await new Promise(resolve => setTimeout(resolve, delay));
      
      // Check auth status
      const authResponse = await checkAuth();
      
      if (!authResponse.is_admin) {
        setError(authResponse.message);
      }
    } catch (err) {
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container>
      {isLoading ? (
        <LoadingSpinner text="Generating leads..." />
      ) : (
        <>
          <Button 
            onClick={handleGenerateLeads}
            disabled={isLoading}
          >
            Generate Leads
          </Button>
          {error && <ErrorMessage>{error}</ErrorMessage>}
        </>
      )}
    </Container>
  );
};

export default LeadGeneration; 