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
} from '@mui/material';
import { styled } from '@mui/material/styles';
import FeatureIcon from '../components/FeatureIcon';
import FadeInSection from '../components/FadeInSection';

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

const DataSourceCard = styled(Card)(({ theme }) => ({
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  textAlign: 'center',
  padding: theme.spacing(4),
  cursor: 'pointer',
  border: `2px solid transparent`,
  '&:hover': {
    borderColor: theme.palette.primary.main,
    transform: 'translateY(-4px)',
    boxShadow: '0px 8px 24px rgba(0, 0, 0, 0.08)',
  },
  '&.selected': {
    borderColor: theme.palette.primary.main,
    backgroundColor: 'rgba(255, 107, 61, 0.05)',
  },
}));

const LandingPage: React.FC = () => {
  const theme = useTheme();
  const [selectedSource, setSelectedSource] = React.useState<string | null>(null);

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
      description: 'Access professional networks and business contacts',
      icon: '🔗',
    },
    {
      id: 'google',
      title: 'Google My Business',
      description: 'Find local businesses and their contact information',
      icon: '🌐',
    },
    {
      id: 'bing',
      title: 'Bing Places',
      description: 'Discover business listings and contact details',
      icon: '🔍',
    },
    {
      id: 'yellow-pages',
      title: 'Yellow Pages',
      description: 'Access comprehensive business directories',
      icon: '📒',
    },
    {
      id: 'crunchbase',
      title: 'Crunchbase',
      description: 'Get detailed company and investment data',
      icon: '📊',
    },
  ];

  const handleSourceSelect = (sourceId: string) => {
    setSelectedSource(sourceId);
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
              Choose Your Data Source
            </Typography>
            <Typography variant="h5" align="center" color="text.secondary" sx={{ mb: 8 }}>
              Select where you want to find your ideal customers
            </Typography>
          </FadeInSection>
          
          <Grid container spacing={4}>
            {dataSources.map((source, index) => (
              <Grid item xs={12} sm={6} md={4} lg={2.4} key={source.id}>
                <FadeInSection delay={index * 0.1}>
                  <DataSourceCard
                    className={selectedSource === source.id ? 'selected' : ''}
                    onClick={() => handleSourceSelect(source.id)}
                  >
                    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                      <FeatureIcon icon={source.icon} />
                      <Typography variant="h6" gutterBottom>
                        {source.title}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {source.description}
                      </Typography>
                    </Box>
                  </DataSourceCard>
                </FadeInSection>
              </Grid>
            ))}
          </Grid>
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

export default LandingPage; 