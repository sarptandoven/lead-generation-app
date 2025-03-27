import React, { useEffect, useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Alert,
} from '@mui/material';
import { dataSourceService, type Lead } from '../services/dataSourceService';
import { useNavigate } from 'react-router-dom';

const ResultsPage: React.FC = () => {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchLeads = async () => {
      try {
        const loadingStartTime = parseInt(localStorage.getItem('loadingStartTime') || '0');
        const currentTime = Date.now();
        const elapsedTime = currentTime - loadingStartTime;
        const minimumLoadingTime = 5000; // 5 seconds

        // If not enough time has passed, go back to loading page
        if (elapsedTime < minimumLoadingTime) {
          navigate('/loading');
          return;
        }

        const searchCriteria = JSON.parse(localStorage.getItem('searchCriteria') || '{}');
        const { leads: fetchedLeads } = await dataSourceService.searchLeads(
          ['linkedin', 'airbnb'],
          {
            query: searchCriteria.targetCity,
            location: [searchCriteria.state],
            companySize: [searchCriteria.propertyCount],
            limit: parseInt(searchCriteria.leadCount),
          }
        );
        setLeads(fetchedLeads);
      } catch (err: any) {
        setError('You do not have admin access to search contact profiles.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchLeads();
  }, [navigate]);

  const handleExport = () => {
    // Implement export functionality
    console.log('Exporting leads...');
  };

  if (isLoading) {
    return (
      <Container>
        <Typography variant="h4" component="h1" gutterBottom>
          Loading Results...
        </Typography>
      </Container>
    );
  }

  if (error) {
    return (
      <Container>
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
        <Box mt={2} textAlign="center">
          <Button variant="contained" color="primary" onClick={() => navigate('/')}>
            Back to Search
          </Button>
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Typography variant="h4" component="h1">
          Your Leads
        </Typography>
        <Button variant="contained" color="primary" onClick={handleExport}>
          Export to CSV
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Phone</TableCell>
              <TableCell>Location</TableCell>
              <TableCell>Source</TableCell>
              <TableCell>Quality Score</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {leads.map((lead, index) => (
              <TableRow key={index}>
                <TableCell>{`${lead.firstName} ${lead.lastName}`.trim() || '-'}</TableCell>
                <TableCell>{lead.email || '-'}</TableCell>
                <TableCell>{lead.phone || '-'}</TableCell>
                <TableCell>{lead.location || '-'}</TableCell>
                <TableCell>{lead.source}</TableCell>
                <TableCell>{lead.qualityScore}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
};

export default ResultsPage; 