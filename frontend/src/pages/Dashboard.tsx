import React, { useEffect, useState } from 'react';
import {
  Box,
  Container,
  Grid,
  Heading,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Badge,
  Progress,
  Card,
  CardHeader,
  CardBody,
  Text,
  Select,
  HStack,
  Icon,
  Button,
  useToast,
  BadgeProps,
} from '@chakra-ui/react';
import { FaUserTie, FaChartLine, FaRobot, FaSpinner } from 'react-icons/fa';
import axios from 'axios';

interface Lead {
  id: string;
  name: string;
  company: string;
  position: string;
  score: number;
  status: 'new' | 'contacted' | 'qualified' | 'converted';
  source: string;
  lastActivity: string;
}

interface LeadInsight {
  category: string;
  score: number;
  recommendation: string;
}

type StatusColorScheme = {
  [K in Lead['status']]: BadgeProps['colorScheme'];
};

const Dashboard: React.FC = () => {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [insights, setInsights] = useState<LeadInsight[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [timeframe, setTimeframe] = useState<string>('7d');
  const toast = useToast();

  const statusColorScheme: StatusColorScheme = {
    new: 'blue',
    contacted: 'yellow',
    qualified: 'green',
    converted: 'purple',
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        // In a real implementation, these would be actual API endpoints
        const [leadsResponse, insightsResponse] = await Promise.all([
          axios.get<Lead[]>('/api/leads'),
          axios.get<LeadInsight[]>('/api/insights'),
        ]);

        setLeads(leadsResponse.data);
        setInsights(insightsResponse.data);
      } catch (error) {
        toast({
          title: 'Error fetching data',
          description: 'Please try again later',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [timeframe, toast]);

  const stats = {
    totalLeads: leads.length,
    qualifiedLeads: leads.filter(l => l.status === 'qualified').length,
    conversionRate: leads.length ? 
      (leads.filter(l => l.status === 'converted').length / leads.length * 100).toFixed(1) : 
      '0',
    averageScore: leads.length ? 
      (leads.reduce((acc, curr) => acc + curr.score, 0) / leads.length).toFixed(1) : 
      '0',
  };

  return (
    <Container maxW="container.xl" py={8}>
      <HStack justify="space-between" mb={8}>
        <Heading size="lg">Lead Generation Dashboard</Heading>
        <Select
          w="200px"
          value={timeframe}
          onChange={(e) => setTimeframe(e.target.value)}
        >
          <option value="7d">Last 7 Days</option>
          <option value="30d">Last 30 Days</option>
          <option value="90d">Last 90 Days</option>
        </Select>
      </HStack>

      {/* Stats Grid */}
      <Grid templateColumns={{ base: '1fr', md: 'repeat(4, 1fr)' }} gap={6} mb={8}>
        <Stat>
          <Card>
            <CardBody>
              <StatLabel>Total Leads</StatLabel>
              <StatNumber>{stats.totalLeads}</StatNumber>
              <StatHelpText>
                <StatArrow type="increase" />
                23.36%
              </StatHelpText>
            </CardBody>
          </Card>
        </Stat>

        <Stat>
          <Card>
            <CardBody>
              <StatLabel>Qualified Leads</StatLabel>
              <StatNumber>{stats.qualifiedLeads}</StatNumber>
              <StatHelpText>
                <StatArrow type="increase" />
                9.05%
              </StatHelpText>
            </CardBody>
          </Card>
        </Stat>

        <Stat>
          <Card>
            <CardBody>
              <StatLabel>Conversion Rate</StatLabel>
              <StatNumber>{stats.conversionRate}%</StatNumber>
              <StatHelpText>
                <StatArrow type="increase" />
                5.42%
              </StatHelpText>
            </CardBody>
          </Card>
        </Stat>

        <Stat>
          <Card>
            <CardBody>
              <StatLabel>Average Lead Score</StatLabel>
              <StatNumber>{stats.averageScore}</StatNumber>
              <StatHelpText>
                <StatArrow type="increase" />
                12.75%
              </StatHelpText>
            </CardBody>
          </Card>
        </Stat>
      </Grid>

      {/* AI Insights */}
      <Card mb={8}>
        <CardHeader>
          <HStack>
            <Icon as={FaRobot} />
            <Heading size="md">AI-Generated Insights</Heading>
          </HStack>
        </CardHeader>
        <CardBody>
          <Grid templateColumns={{ base: '1fr', md: 'repeat(3, 1fr)' }} gap={6}>
            {insights.map((insight, index) => (
              <Box key={index} p={4} borderWidth="1px" borderRadius="lg">
                <Text fontWeight="bold" mb={2}>{insight.category}</Text>
                <Progress value={insight.score * 100} colorScheme="blue" mb={2} />
                <Text fontSize="sm" color="gray.600">{insight.recommendation}</Text>
              </Box>
            ))}
          </Grid>
        </CardBody>
      </Card>

      {/* Recent Leads Table */}
      <Card>
        <CardHeader>
          <HStack justify="space-between">
            <Heading size="md">Recent Leads</Heading>
            <Button colorScheme="blue" leftIcon={<Icon as={FaSpinner} />}>
              Refresh Data
            </Button>
          </HStack>
        </CardHeader>
        <CardBody overflowX="auto">
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>Name</Th>
                <Th>Company</Th>
                <Th>Position</Th>
                <Th>Score</Th>
                <Th>Status</Th>
                <Th>Source</Th>
                <Th>Last Activity</Th>
              </Tr>
            </Thead>
            <Tbody>
              {leads.map((lead) => (
                <Tr key={lead.id}>
                  <Td fontWeight="medium">{lead.name}</Td>
                  <Td>{lead.company}</Td>
                  <Td>{lead.position}</Td>
                  <Td>
                    <Badge
                      colorScheme={lead.score >= 80 ? 'green' : lead.score >= 60 ? 'yellow' : 'red'}
                      variant="subtle"
                      px={2}
                      py={1}
                      rounded="full"
                    >
                      {lead.score}
                    </Badge>
                  </Td>
                  <Td>
                    <Badge colorScheme={statusColorScheme[lead.status]}>
                      {lead.status}
                    </Badge>
                  </Td>
                  <Td>{lead.source}</Td>
                  <Td>{lead.lastActivity}</Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        </CardBody>
      </Card>
    </Container>
  );
};

export default Dashboard; 