import React from 'react';
import styled, { keyframes } from 'styled-components';

const spin = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

const pulse = keyframes`
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
`;

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
`;

const SpinnerWrapper = styled.div`
  position: relative;
  width: 80px;
  height: 80px;
  margin-bottom: 20px;
`;

const Spinner = styled.div`
  position: absolute;
  width: 100%;
  height: 100%;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: ${spin} 1s linear infinite;
`;

const InnerSpinner = styled(Spinner)`
  width: 60%;
  height: 60%;
  top: 20%;
  left: 20%;
  border-top-color: #e74c3c;
  animation-direction: reverse;
`;

const LoadingText = styled.div`
  font-size: 1.2rem;
  color: #333;
  margin-top: 20px;
  animation: ${pulse} 1.5s ease-in-out infinite;
`;

interface Props {
  text?: string;
}

const LoadingSpinner: React.FC<Props> = ({ text = "Processing your request..." }) => {
  return (
    <Container>
      <SpinnerWrapper>
        <Spinner />
        <InnerSpinner />
      </SpinnerWrapper>
      <LoadingText>{text}</LoadingText>
    </Container>
  );
};

export default LoadingSpinner; 