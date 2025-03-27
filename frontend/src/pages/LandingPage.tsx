import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  TextField,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  styled,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import TrustedCompanies from '../components/TrustedCompanies';

const StyledContainer = styled(Container)(({ theme }) => ({
  marginTop: theme.spacing(8),
  marginBottom: theme.spacing(8),
  textAlign: 'center',
}));

const FormSection = styled(Box)(({ theme }) => ({
  maxWidth: '1000px',
  margin: '0 auto',
  marginTop: theme.spacing(6),
  padding: theme.spacing(4),
  backgroundColor: '#fff',
  borderRadius: theme.shape.borderRadius,
  boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.05)',
}));

const FormGrid = styled(Box)(({ theme }) => ({
  display: 'grid',
  gridTemplateColumns: 'repeat(2, 1fr)',
  gap: theme.spacing(3),
  marginTop: theme.spacing(4),
  [theme.breakpoints.down('sm')]: {
    gridTemplateColumns: '1fr',
  },
}));

const LandingPage = () => {
  const [propertyCount, setPropertyCount] = useState('1-7');
  const [targetCity, setTargetCity] = useState('');
  const [state, setState] = useState('');
  const [leadCount, setLeadCount] = useState('25');
  const navigate = useNavigate();

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    // Store search criteria in localStorage
    localStorage.setItem('searchCriteria', JSON.stringify({
      propertyCount,
      targetCity,
      state,
      leadCount
    }));
    // Navigate to loading page
    navigate('/loading');
  };

  return (
    <StyledContainer>
      <Typography
        variant="h1"
        sx={{
          fontSize: { xs: '2.5rem', md: '4rem' },
          fontWeight: 'bold',
          mb: 2,
        }}
      >
        Get The <span style={{ color: '#FF6B3D' }}>Leads</span> You Need
      </Typography>
      
      <Typography
        variant="h2"
        sx={{
          fontSize: { xs: '1.25rem', md: '1.75rem' },
          color: 'text.secondary',
          mb: 6,
        }}
      >
        Connect with property managers who are ready to scale
      </Typography>

      <FormSection>
        <form onSubmit={handleSubmit}>
          <FormGrid>
            <FormControl fullWidth>
              <InputLabel>Properties Under Management</InputLabel>
              <Select
                value={propertyCount}
                label="Properties Under Management"
                onChange={(e) => setPropertyCount(e.target.value)}
              >
                <MenuItem value="1-7">1-7 properties</MenuItem>
                <MenuItem value="8-15">8-15 properties</MenuItem>
                <MenuItem value="16-30">16-30 properties</MenuItem>
                <MenuItem value="31+">31+ properties</MenuItem>
              </Select>
            </FormControl>

            <TextField
              fullWidth
              label="Target City"
              placeholder="e.g., San Francisco"
              value={targetCity}
              onChange={(e) => setTargetCity(e.target.value)}
            />

            <FormControl fullWidth>
              <InputLabel>State Focus</InputLabel>
              <Select
                value={state}
                label="State Focus"
                onChange={(e) => setState(e.target.value)}
              >
                <MenuItem value="CA">California</MenuItem>
                <MenuItem value="NY">New York</MenuItem>
                <MenuItem value="TX">Texas</MenuItem>
                <MenuItem value="FL">Florida</MenuItem>
                {/* Add more states as needed */}
              </Select>
            </FormControl>

            <TextField
              fullWidth
              label="Lead Count"
              type="number"
              value={leadCount}
              onChange={(e) => setLeadCount(e.target.value)}
              InputProps={{ inputProps: { min: 1, max: 100 } }}
            />
          </FormGrid>

          <Button
            variant="contained"
            size="large"
            type="submit"
            sx={{
              mt: 6,
              mb: 2,
              py: 2,
              px: 6,
              borderRadius: '50px',
              backgroundColor: '#FF6B3D',
              '&:hover': {
                backgroundColor: '#E85A2C',
              },
            }}
          >
            Generate Leads
          </Button>
        </form>
      </FormSection>

      <Box sx={{ mt: 12, mb: 6 }}>
        <Typography
          variant="h2"
          sx={{
            fontSize: { xs: '2rem', md: '3rem' },
            fontWeight: 'bold',
            textAlign: 'center',
          }}
        >
          Companies <span style={{ color: '#FF6B3D' }}>Trust</span> Our Leads
        </Typography>
        <TrustedCompanies />
      </Box>
    </StyledContainer>
  );
};

export default LandingPage; 