import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  CircularProgress,
  Card,
  CardContent,
  CardHeader,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Button,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  People as PeopleIcon,
  Business as BusinessIcon,
  LocationOn as LocationIcon,
  Email as EmailIcon,
  Phone as PhoneIcon,
} from '@mui/icons-material';

interface DashboardStats {
  totalLeads: number;
  newLeads: number;
  qualifiedLeads: number;
  conversionRate: number;
  topLocations: Array<{ location: string; count: number }>;
  recentLeads: Array<{
    id: string;
    name: string;
    company: string;
    location: string;
    status: string;
    date: string;
  }>;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats>({
    totalLeads: 0,
    newLeads: 0,
    qualifiedLeads: 0,
    conversionRate: 0,
    topLocations: [],
    recentLeads: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      const response = await fetch('http://localhost:8000/dashboard/stats', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch dashboard stats');
      }

      const data = await response.json();
      setStats(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={3}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* Key Metrics */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <PeopleIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">Total Leads</Typography>
              </Box>
              <Typography variant="h4">{stats.totalLeads}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <TrendingUpIcon color="success" sx={{ mr: 1 }} />
                <Typography variant="h6">New Leads</Typography>
              </Box>
              <Typography variant="h4">{stats.newLeads}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <BusinessIcon color="info" sx={{ mr: 1 }} />
                <Typography variant="h6">Qualified Leads</Typography>
              </Box>
              <Typography variant="h4">{stats.qualifiedLeads}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <TrendingUpIcon color="warning" sx={{ mr: 1 }} />
                <Typography variant="h6">Conversion Rate</Typography>
              </Box>
              <Typography variant="h4">{stats.conversionRate}%</Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Top Locations */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="Top Locations" />
            <CardContent>
              <List>
                {stats.topLocations.map((location, index) => (
                  <React.Fragment key={location.location}>
                    <ListItem>
                      <ListItemIcon>
                        <LocationIcon color="primary" />
                      </ListItemIcon>
                      <ListItemText
                        primary={location.location}
                        secondary={`${location.count} leads`}
                      />
                    </ListItem>
                    {index < stats.topLocations.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Leads */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader
              title="Recent Leads"
              action={
                <Button color="primary" size="small">
                  View All
                </Button>
              }
            />
            <CardContent>
              <List>
                {stats.recentLeads.map((lead, index) => (
                  <React.Fragment key={lead.id}>
                    <ListItem>
                      <ListItemIcon>
                        <PeopleIcon color="primary" />
                      </ListItemIcon>
                      <ListItemText
                        primary={lead.name}
                        secondary={
                          <Box>
                            <Typography variant="body2" component="span">
                              {lead.company}
                            </Typography>
                            <Typography variant="body2" color="textSecondary" component="span">
                              {' • '}
                              {lead.location}
                            </Typography>
                          </Box>
                        }
                      />
                    </ListItem>
                    {index < stats.recentLeads.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 