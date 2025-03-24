import React from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
} from '@mui/material';
import {
  TrendingUp,
  People,
  BusinessCenter,
  Assessment,
} from '@mui/icons-material';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  color: string;
}

const StatCard: React.FC<StatCardProps> = ({ title, value, icon, color }) => (
  <Card>
    <CardContent>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h6" component="div">
            {value}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {title}
          </Typography>
        </Box>
        <Box sx={{ 
          backgroundColor: `${color}20`,
          borderRadius: '50%',
          padding: 1,
          display: 'flex'
        }}>
          {React.cloneElement(icon as React.ReactElement, { sx: { color } })}
        </Box>
      </Box>
    </CardContent>
  </Card>
);

const Dashboard: React.FC = () => {
  const stats = [
    {
      title: 'Total Leads',
      value: '2,345',
      icon: <People />,
      color: '#2196f3'
    },
    {
      title: 'Conversion Rate',
      value: '12.3%',
      icon: <TrendingUp />,
      color: '#4caf50'
    },
    {
      title: 'Active Campaigns',
      value: '8',
      icon: <BusinessCenter />,
      color: '#ff9800'
    },
    {
      title: 'Success Rate',
      value: '67%',
      icon: <Assessment />,
      color: '#9c27b0'
    }
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <StatCard {...stat} />
          </Grid>
        ))}
      </Grid>

      <Box sx={{ mt: 4 }}>
        <Typography variant="h5" component="h2" gutterBottom>
          Recent Activity
        </Typography>
        <Card>
          <CardContent>
            <Typography variant="body1">
              Activity feed coming soon...
            </Typography>
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
};

export default Dashboard; 