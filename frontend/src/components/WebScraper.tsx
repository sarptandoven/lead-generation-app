import React, { useState, useEffect, ChangeEvent, FormEvent } from 'react';
import {
  Box,
  Container,
  Flex,
  Heading,
  Text,
  Badge,
  VStack,
  Stack,
  Input,
  Checkbox,
  Button,
  Progress,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  FormControl,
  FormLabel,
  useToast,
} from '@chakra-ui/react';
import { motion, AnimatePresence } from 'framer-motion';
import { apiService, type Lead } from '../services/api';

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

interface Sources {
  linkedin: boolean;
  airbnb: boolean;
  customWebsite: boolean;
}

const WebScraper: React.FC = () => {
  const [sources, setSources] = useState<Sources>({
    linkedin: false,
    airbnb: false,
    customWebsite: false,
  });
  const [customUrl, setCustomUrl] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [location, setLocation] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentPhraseIndex, setCurrentPhraseIndex] = useState(0);
  const [leads, setLeads] = useState<Lead[]>([]);
  const toast = useToast();

  useEffect(() => {
    if (isLoading) {
      const interval = setInterval(() => {
        setCurrentPhraseIndex((prevIndex) => (prevIndex + 1) % rotatingPhrases.length);
        setProgress((prevProgress) => Math.min(prevProgress + 5, 95));
      }, 2000);

      return () => clearInterval(interval);
    } else {
      setProgress(0);
    }
  }, [isLoading]);

  const handleSourceChange = (source: keyof Sources) => {
    setSources((prev) => ({
      ...prev,
      [source]: !prev[source],
    }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    
    const selectedSources: string[] = [
      ...(sources.linkedin ? ['linkedin'] : []),
      ...(sources.airbnb ? ['airbnb'] : []),
      ...(sources.customWebsite && customUrl ? [customUrl] : []),
    ];

    if (selectedSources.length === 0) {
      toast({
        title: 'Error',
        description: 'Please select at least one source',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setIsLoading(true);
    try {
      const response = await apiService.scrapeSource(selectedSources, searchQuery);
      setLeads(response.leads);
      
      toast({
        title: 'Success',
        description: `Found ${response.totalFound} leads`,
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      
    } catch (error) {
      toast({
        title: 'Error',
        description: error instanceof Error ? error.message : 'An error occurred',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleExport = async () => {
    try {
      await apiService.exportToCSV(leads);
      toast({
        title: 'Success',
        description: 'Leads exported to CSV',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to export leads',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const getQualityScoreBadge = (score: number) => {
    let color = 'red';
    if (score >= 0.8) color = 'green';
    else if (score >= 0.6) color = 'yellow';
    else if (score >= 0.4) color = 'orange';
    
    return (
      <Badge colorScheme={color} fontSize="sm">
        {Math.round(score * 100)}%
      </Badge>
    );
  };

  return (
    <Container maxW="container.xl" py={8}>
      <VStack spacing={8} align="stretch">
        <Heading as="h1" size="xl" textAlign="center" mb={8}>
          Sarp Scout
        </Heading>

        <Box as="form" onSubmit={handleSubmit}>
          <Stack spacing={6}>
            <FormControl>
              <FormLabel>Search Query</FormLabel>
              <Input
                value={searchQuery}
                onChange={(e: ChangeEvent<HTMLInputElement>) => setSearchQuery(e.target.value)}
                placeholder="Enter search terms..."
                isDisabled={isLoading}
              />
            </FormControl>

            <FormControl>
              <FormLabel>Location (optional)</FormLabel>
              <Input
                value={location}
                onChange={(e: ChangeEvent<HTMLInputElement>) => setLocation(e.target.value)}
                placeholder="Enter location..."
                isDisabled={isLoading}
              />
            </FormControl>

            <FormControl>
              <FormLabel>Select Sources</FormLabel>
              <Stack spacing={3}>
                <Checkbox
                  isChecked={sources.linkedin}
                  onChange={() => handleSourceChange('linkedin')}
                  isDisabled={isLoading}
                >
                  LinkedIn
                </Checkbox>
                <Checkbox
                  isChecked={sources.airbnb}
                  onChange={() => handleSourceChange('airbnb')}
                  isDisabled={isLoading}
                >
                  Airbnb
                </Checkbox>
                <Checkbox
                  isChecked={sources.customWebsite}
                  onChange={() => handleSourceChange('customWebsite')}
                  isDisabled={isLoading}
                >
                  Custom Website
                </Checkbox>
                {sources.customWebsite && (
                  <Input
                    value={customUrl}
                    onChange={(e: ChangeEvent<HTMLInputElement>) => setCustomUrl(e.target.value)}
                    placeholder="Enter website URL..."
                    isDisabled={isLoading}
                  />
                )}
              </Stack>
            </FormControl>

            <Button
              type="submit"
              colorScheme="blue"
              isDisabled={isLoading}
              isLoading={isLoading}
            >
              Start Scraping
            </Button>
          </Stack>
        </Box>

        {isLoading && (
          <Box>
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
        )}

        {leads.length > 0 && (
          <Box>
            <Flex justify="space-between" align="center" mb={4}>
              <Heading size="md">Results ({leads.length} leads found)</Heading>
              <Button onClick={handleExport} colorScheme="green" size="sm">
                Export to CSV
              </Button>
            </Flex>

            <Box overflowX="auto">
              <Table variant="simple">
                <Thead>
                  <Tr>
                    <Th>Name</Th>
                    <Th>Email</Th>
                    <Th>Phone</Th>
                    <Th>Location</Th>
                    <Th>Source</Th>
                    <Th>Quality</Th>
                  </Tr>
                </Thead>
                <Tbody>
                  {leads.map((lead, index) => (
                    <Tr key={index}>
                      <Td>{`${lead.firstName} ${lead.lastName}`.trim() || '-'}</Td>
                      <Td>{lead.email || '-'}</Td>
                      <Td>{lead.phone || '-'}</Td>
                      <Td>{lead.location || '-'}</Td>
                      <Td>{lead.source}</Td>
                      <Td>{getQualityScoreBadge(lead.qualityScore)}</Td>
                    </Tr>
                  ))}
                </Tbody>
              </Table>
            </Box>
          </Box>
        )}
      </VStack>
    </Container>
  );
};

export default WebScraper; 