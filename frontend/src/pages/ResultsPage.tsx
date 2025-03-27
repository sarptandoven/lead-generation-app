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

const ResultsPage: React.FC = () => {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchLeads = async () => {
      try {
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
        setError(err.message || 'An error occurred while fetching leads.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchLeads();
  }, []);

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