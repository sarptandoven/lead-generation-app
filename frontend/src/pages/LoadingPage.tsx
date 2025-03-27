import React, { useEffect, useState } from 'react';
import { Box, Container, Text, Progress, VStack, Heading } from '@chakra-ui/react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

const rotatingPhrases = [
  "Discovering high-quality leads...",
  "Analyzing contact information...",
  "Evaluating lead potential...",
  "Filtering for best matches...",
  "Enriching lead data...",
  "Validating contact details...",
  "Calculating quality scores...",
  "Preparing insights...",
];

const LoadingPage: React.FC = () => {
  const [progress, setProgress] = useState(0);
  const [currentPhraseIndex, setCurrentPhraseIndex] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    // Store the start time in localStorage
    localStorage.setItem('loadingStartTime', Date.now().toString());

    const interval = setInterval(() => {
      setCurrentPhraseIndex((prevIndex) => (prevIndex + 1) % rotatingPhrases.length);
      setProgress((prevProgress) => Math.min(prevProgress + 5, 95));
    }, 2000);

    // Random delay between 5-15 seconds
    const delay = Math.random() * 10000 + 5000;
    const timeout = setTimeout(() => {
      clearInterval(interval);
      setProgress(100);
      // Navigate to results page after a short delay
      setTimeout(() => {
        navigate('/results');
      }, 1000);
    }, delay);

    return () => {
      clearInterval(interval);
      clearTimeout(timeout);
    };
  }, [navigate]);

  return (
    <Container maxW="container.md" py={20}>
      <VStack spacing={8} align="center">
        <Heading as="h1" size="xl" textAlign="center">
          Finding Your Leads
        </Heading>
        
        <Box w="full">
          <Progress value={progress} size="sm" colorScheme="blue" mb={4} />
          <AnimatePresence mode="wait">
            <motion.div
              key={currentPhraseIndex}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
            >
              <Text textAlign="center" fontSize="lg" color="blue.500">
                {rotatingPhrases[currentPhraseIndex]}
              </Text>
            </motion.div>
          </AnimatePresence>
        </Box>
      </VStack>
    </Container>
  );
};

export default LoadingPage; 