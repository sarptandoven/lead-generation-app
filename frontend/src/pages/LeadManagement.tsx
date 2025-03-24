import React, { useState } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Chip,
  Box,
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Email as EmailIcon,
  Phone as PhoneIcon,
} from '@mui/icons-material';

interface Lead {
  id: string;
  name: string;
  company: string;
  email: string;
  phone: string;
  status: string;
  source: string;
  dateAdded: string;
}

const LeadManagement: React.FC = () => {
  const [leads] = useState<Lead[]>([
    {
      id: '1',
      name: 'John Doe',
      company: 'Tech Corp',
      email: 'john@techcorp.com',
      phone: '+1-234-567-8900',
      status: 'New',
      source: 'LinkedIn',
      dateAdded: '2024-03-20',
    },
    {
      id: '2',
      name: 'Jane Smith',
      company: 'Property Management Inc',
      email: 'jane@pmi.com',
      phone: '+1-234-567-8901',
      status: 'Contacted',
      source: 'Airbnb',
      dateAdded: '2024-03-19',
    },
  ]);

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'new':
        return 'primary';
      case 'contacted':
        return 'info';
      case 'qualified':
        return 'success';
      case 'lost':
        return 'error';
      default:
        return 'default';
    }
  };

  const handleEdit = (id: string) => {
    console.log('Edit lead:', id);
  };

  const handleDelete = (id: string) => {
    console.log('Delete lead:', id);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Lead Management
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Name</TableCell>
                      <TableCell>Company</TableCell>
                      <TableCell>Contact</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Source</TableCell>
                      <TableCell>Date Added</TableCell>
                      <TableCell>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {leads.map((lead) => (
                      <TableRow key={lead.id}>
                        <TableCell>{lead.name}</TableCell>
                        <TableCell>{lead.company}</TableCell>
                        <TableCell>
                          <Box sx={{ display: 'flex', gap: 1 }}>
                            <IconButton size="small" href={`mailto:${lead.email}`}>
                              <EmailIcon fontSize="small" />
                            </IconButton>
                            <IconButton size="small" href={`tel:${lead.phone}`}>
                              <PhoneIcon fontSize="small" />
                            </IconButton>
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={lead.status}
                            color={getStatusColor(lead.status)}
                            size="small"
                          />
                        </TableCell>
                        <TableCell>{lead.source}</TableCell>
                        <TableCell>{lead.dateAdded}</TableCell>
                        <TableCell>
                          <IconButton size="small" onClick={() => handleEdit(lead.id)}>
                            <EditIcon fontSize="small" />
                          </IconButton>
                          <IconButton size="small" onClick={() => handleDelete(lead.id)}>
                            <DeleteIcon fontSize="small" />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default LeadManagement; 