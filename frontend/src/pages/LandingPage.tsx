import React from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  Rating,
  Avatar,
  useTheme,
  IconButton,
  Dialog,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import FeatureIcon from '../components/FeatureIcon';
import FadeInSection from '../components/FadeInSection';
import DataSourceSelector from '../components/DataSourceSelector';
import DataSourceConfig from '../components/DataSourceConfig';
import { DataSourceProvider, useDataSources } from '../contexts/DataSourceContext';
import LinkedInIcon from '@mui/icons-material/LinkedIn';
import BusinessIcon from '@mui/icons-material/Business';
import SearchIcon from '@mui/icons-material/Search';
import ContactPageIcon from '@mui/icons-material/ContactPage';
import BusinessCenterIcon from '@mui/icons-material/BusinessCenter';
import WorkIcon from '@mui/icons-material/Work';

// Custom styled components
const HeroSection = styled(Box)(({ theme }) => ({
  position: 'relative',
  padding: theme.spacing(12, 0),
  background: '#FFFFFF',
  overflow: 'hidden',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundImage: 'url("/illustrations/hero-bg.svg")',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
    backgroundSize: 'cover',
    opacity: 0.1,
  },
}));

const FeatureCard = styled(Card)(({ theme }) => ({
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  textAlign: 'center',
  padding: theme.spacing(4),
}));

const TestimonialCard = styled(Card)(({ theme }) => ({
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  padding: theme.spacing(3),
}));

const LandingPageContent: React.FC = () => {
  const theme = useTheme();
  const { selectedSources, setSelectedSources, sourceConfigs } = useDataSources();
  const [configureSource, setConfigureSource] = React.useState<string | null>(null);

  const features = [
    {
      title: 'Smart Search',
      description: 'Advanced algorithms to find the perfect leads for your business',
      icon: '🔍',
    },
    {
      title: 'Real-time Updates',
      description: 'Stay informed with instant notifications and updates',
      icon: '⚡',
    },
    {
      title: 'Data Analytics',
      description: 'Powerful insights to optimize your lead generation strategy',
      icon: '📊',
    },
  ];

  const testimonials = [
    {
      name: 'Sarah Johnson',
      role: 'Sales Director',
      company: 'TechCorp',
      avatar: '/avatars/avatar1.jpg',
      comment: 'This tool has transformed how we generate and manage leads.',
      rating: 5,
    },
    {
      name: 'Michael Chen',
      role: 'Marketing Manager',
      company: 'GrowthCo',
      avatar: '/avatars/avatar2.jpg',
      comment: 'Incredibly intuitive and powerful. A game-changer for our team.',
      rating: 5,
    },
  ];

  const dataSources = [
    {
      id: 'linkedin',
      title: 'LinkedIn',
      description: 'Find leads from professional networks',
      icon: LinkedInIcon,
    },
    {
      id: 'google',
      title: 'Google My Business',
      description: 'Discover local businesses and contacts',
      icon: BusinessIcon,
    },
    {
      id: 'bing',
      title: 'Bing Places',
      description: 'Access business listings and contact information',
      icon: SearchIcon,
    },
    {
      id: 'yellow-pages',
      title: 'Yellow Pages',
      description: 'Search business directories for leads',
      icon: ContactPageIcon,
    },
    {
      id: 'crunchbase',
      title: 'Crunchbase',
      description: 'Get data on companies and key personnel',
      icon: BusinessCenterIcon,
    },
    {
      id: 'role-based',
      title: 'Role/Job Title',
      description: 'Filter leads by specific roles and titles',
      icon: WorkIcon,
    },
  ];

  const handleSourcesChange = (sources: string[]) => {
    setSelectedSources(sources);
    
    // Check if any newly selected source needs configuration
    const newSources = sources.filter(s => !selectedSources.includes(s));
    if (newSources.length > 0) {
      const unconfiguredSource = newSources.find(s => sourceConfigs[s]?.status !== 'configured');
      if (unconfiguredSource) {
        setConfigureSource(unconfiguredSource);
      }
    }
  };

  const handleConfigured = () => {
    setConfigureSource(null);
  };

  return (
    <Box>
      <HeroSection>
        <Container maxWidth="lg">
          <Grid container spacing={6} alignItems="center">
            <Grid item xs={12} md={6}>
              <FadeInSection direction="left">
                <Typography variant="h1" gutterBottom>
                  Supercharge Your Lead Generation
                </Typography>
                <Typography variant="h4" color="text.secondary" sx={{ mb: 4 }}>
                  Find and connect with your ideal customers using AI-powered insights
                </Typography>
            <Button
                  variant="contained"
                  size="large"
                  sx={{ mr: 2 }}
            >
              Get Started
            </Button>
            <Button
                  variant="outlined"
                  size="large"
                >
                  Learn More
            </Button>
              </FadeInSection>
            </Grid>
            <Grid item xs={12} md={6}>
              <FadeInSection direction="right">
                <Box
                  component="img"
                  src="/illustrations/hero-main.svg"
                  alt="Lead Generation Platform"
                  sx={{
                    width: '100%',
                    height: 'auto',
                    maxWidth: 600,
                    filter: 'drop-shadow(0px 10px 20px rgba(0, 0, 0, 0.1))',
                    animation: 'float 6s ease-in-out infinite',
                    '@keyframes float': {
                      '0%, 100%': {
                        transform: 'translateY(0)',
                      },
                      '50%': {
                        transform: 'translateY(-20px)',
                      },
                    },
                  }}
                />
              </FadeInSection>
            </Grid>
          </Grid>
        </Container>
      </HeroSection>

      <Box sx={{ py: 12, backgroundColor: 'background.paper' }}>
        <Container maxWidth="lg">
          <FadeInSection>
            <Typography variant="h2" align="center" gutterBottom>
              Choose Your Data Sources
            </Typography>
            <Typography variant="h5" align="center" color="text.secondary" sx={{ mb: 4 }}>
              Select one or more sources to find your ideal customers
            </Typography>
            <Typography variant="body1" align="center" color="text.secondary" sx={{ mb: 8 }}>
              Combine multiple sources to get comprehensive lead data and insights
            </Typography>
          </FadeInSection>
          
          <FadeInSection>
            <DataSourceSelector
              selectedSources={selectedSources}
              onSourcesChange={handleSourcesChange}
            />
          </FadeInSection>

          {selectedSources.length > 0 && (
            <FadeInSection>
              <Box sx={{ mt: 4, textAlign: 'center' }}>
                <Button
                  variant="contained"
                  size="large"
                  onClick={() => {
                    // Check if all selected sources are configured
                    const unconfiguredSource = selectedSources.find(
                      s => sourceConfigs[s]?.status !== 'configured'
                    );
                    if (unconfiguredSource) {
                      setConfigureSource(unconfiguredSource);
                    } else {
                      // Proceed with configured sources
                      console.log('Proceeding with sources:', selectedSources);
                    }
                  }}
                >
                  Continue with {selectedSources.length} {selectedSources.length === 1 ? 'Source' : 'Sources'}
                </Button>
              </Box>
            </FadeInSection>
          )}

          <Dialog
            open={!!configureSource}
            onClose={() => setConfigureSource(null)}
            maxWidth="md"
            fullWidth
          >
            {configureSource && (
              <DataSourceConfig
                sourceId={configureSource}
                onConfigured={handleConfigured}
              />
            )}
          </Dialog>
        </Container>
      </Box>

      <Box sx={{ py: 12, backgroundColor: 'background.paper' }}>
        <Container maxWidth="lg">
          <FadeInSection>
            <Typography variant="h2" align="center" gutterBottom>
              Features Built for Growth
            </Typography>
            <Typography variant="h5" align="center" color="text.secondary" sx={{ mb: 8 }}>
              Everything you need to scale your lead generation efforts
            </Typography>
          </FadeInSection>
          
          <Grid container spacing={4}>
            {features.map((feature, index) => (
              <Grid item xs={12} md={4} key={index}>
                <FadeInSection delay={index * 0.2}>
                  <FeatureCard>
                    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                      <FeatureIcon icon={feature.icon} />
                      <Typography variant="h4" gutterBottom>
                        {feature.title}
                      </Typography>
                      <Typography color="text.secondary" align="center">
                        {feature.description}
                      </Typography>
                    </Box>
                  </FeatureCard>
                </FadeInSection>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      <Box sx={{ py: 12 }}>
        <Container maxWidth="lg">
          <FadeInSection>
            <Typography variant="h2" align="center" gutterBottom>
              Trusted by Industry Leaders
            </Typography>
            <Typography variant="h5" align="center" color="text.secondary" sx={{ mb: 8 }}>
              See what our customers have to say
            </Typography>
          </FadeInSection>

          <Grid container spacing={4}>
            {testimonials.map((testimonial, index) => (
              <Grid item xs={12} md={6} key={index}>
                <FadeInSection direction={index % 2 === 0 ? 'left' : 'right'} delay={index * 0.2}>
                  <TestimonialCard>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Avatar
                        src={testimonial.avatar}
                        sx={{ width: 56, height: 56, mr: 2 }}
                      />
                      <Box>
                        <Typography variant="h6">{testimonial.name}</Typography>
                        <Typography variant="body2" color="text.secondary">
                          {testimonial.role} at {testimonial.company}
                        </Typography>
                      </Box>
                    </Box>
                    <Rating value={testimonial.rating} readOnly sx={{ mb: 2 }} />
                    <Typography variant="body1">
                      "{testimonial.comment}"
                    </Typography>
                  </TestimonialCard>
                </FadeInSection>
              </Grid>
            ))}
          </Grid>
        </Container>
        </Box>

      <Box sx={{ py: 12, backgroundColor: theme.palette.primary.main }}>
        <Container maxWidth="lg">
          <FadeInSection direction="up">
            <Box sx={{ textAlign: 'center', color: 'white' }}>
              <Typography variant="h2" gutterBottom>
                Ready to Get Started?
              </Typography>
              <Typography variant="h5" sx={{ mb: 4, opacity: 0.9 }}>
                Join thousands of companies already using our platform
              </Typography>
            <Button
                variant="contained"
                size="large"
                sx={{
                  backgroundColor: 'white',
                  color: theme.palette.primary.main,
                  '&:hover': {
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                  },
                }}
              >
                Start Free Trial
            </Button>
          </Box>
          </FadeInSection>
        </Container>
          </Box>
    </Box>
  );
};

const LandingPage: React.FC = () => {
  return (
    <DataSourceProvider>
      <LandingPageContent />
    </DataSourceProvider>
  );
};

export default LandingPage; 