import React from 'react';
import {
  Box,
  Grid,
  Typography,
  useTheme,
  styled,
} from '@mui/material';

const CompanyLogo = styled('img')(({ theme }) => ({
  maxWidth: '160px',
  height: 'auto',
  filter: 'grayscale(100%)',
  opacity: 0.7,
  transition: 'all 0.3s ease',
  '&:hover': {
    filter: 'grayscale(0%)',
    opacity: 1,
  },
}));

const companies = [
  {
    name: 'TechCorp',
    logo: '/logos/techcorp.png',
  },
  {
    name: 'InnovatePM',
    logo: '/logos/innovatepm.png',
  },
  {
    name: 'PropTech Solutions',
    logo: '/logos/proptech.png',
  },
  {
    name: 'RealEstate Pro',
    logo: '/logos/realestatepro.png',
  },
  {
    name: 'SmartProperty',
    logo: '/logos/smartproperty.png',
  },
];

const TrustedCompanies = () => {
  const theme = useTheme();

  return (
    <Box sx={{ py: 8 }}>
      <Grid
        container
        spacing={4}
        justifyContent="center"
        alignItems="center"
      >
        {companies.map((company) => (
          <Grid
            item
            key={company.name}
            xs={6}
            sm={4}
            md={2}
            sx={{
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
            }}
          >
            <CompanyLogo
              src={company.logo}
              alt={company.name}
            />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default TrustedCompanies; 