import React from 'react';
import {
  Box,
  Card,
  Typography,
  Checkbox,
  useTheme,
  Chip,
  Tooltip,
  CircularProgress,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import InfoIcon from '@mui/icons-material/Info';

export interface DataSource {
  id: string;
  title: string;
  description: string;
  icon: string;
  capabilities: string[];
  avgResponseTime: string;
  status: 'active' | 'maintenance' | 'limited';
}

interface DataSourceSelectorProps {
  selectedSources: string[];
  onSourcesChange: (sources: string[]) => void;
}

const StyledCard = styled(Card)(({ theme }) => ({
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  padding: theme.spacing(3),
  cursor: 'pointer',
  border: `2px solid transparent`,
  transition: 'all 0.3s ease',
  position: 'relative',
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

const StatusChip = styled(Chip)(({ theme, status }: { theme: any; status: string }) => ({
  position: 'absolute',
  top: 12,
  right: 12,
  backgroundColor: status === 'active' 
    ? theme.palette.success.light 
    : status === 'maintenance'
    ? theme.palette.warning.light
    : theme.palette.error.light,
  color: status === 'active'
    ? theme.palette.success.dark
    : status === 'maintenance'
    ? theme.palette.warning.dark
    : theme.palette.error.dark,
}));

const dataSources: DataSource[] = [
  {
    id: 'linkedin',
    title: 'LinkedIn',
    description: 'Professional network data with detailed company and employee information',
    icon: '🔗',
    capabilities: [
      'Company profiles',
      'Employee data',
      'Job postings',
      'Industry insights'
    ],
    avgResponseTime: '2-3s',
    status: 'active',
  },
  {
    id: 'google',
    title: 'Google My Business',
    description: 'Local business data with contact details and customer reviews',
    icon: '🌐',
    capabilities: [
      'Business listings',
      'Contact information',
      'Customer reviews',
      'Location data'
    ],
    avgResponseTime: '1-2s',
    status: 'active',
  },
  {
    id: 'bing',
    title: 'Bing Places',
    description: 'Business listings with detailed location and service information',
    icon: '🔍',
    capabilities: [
      'Business profiles',
      'Service details',
      'Location data',
      'Contact information'
    ],
    avgResponseTime: '1-2s',
    status: 'maintenance',
  },
  {
    id: 'yellow-pages',
    title: 'Yellow Pages',
    description: 'Comprehensive business directory with industry categorization',
    icon: '📒',
    capabilities: [
      'Business listings',
      'Industry categories',
      'Contact details',
      'Service areas'
    ],
    avgResponseTime: '2-3s',
    status: 'active',
  },
  {
    id: 'crunchbase',
    title: 'Crunchbase',
    description: 'Detailed company data including funding and investment information',
    icon: '📊',
    capabilities: [
      'Company profiles',
      'Funding data',
      'Investment history',
      'Industry analysis'
    ],
    avgResponseTime: '3-4s',
    status: 'active',
  },
  {
    id: 'role-based',
    title: 'Role/Job Title',
    description: 'Filter leads by specific roles and job titles',
    icon: '👥',
    capabilities: [
      'Role filtering',
      'Title matching',
      'Seniority levels',
      'Department targeting'
    ],
    avgResponseTime: '1-2s',
    status: 'active',
  },
];

const DataSourceSelector: React.FC<DataSourceSelectorProps> = ({
  selectedSources,
  onSourcesChange,
}) => {
  const theme = useTheme();

  const handleSourceToggle = (sourceId: string) => {
    const newSelection = selectedSources.includes(sourceId)
      ? selectedSources.filter(id => id !== sourceId)
      : [...selectedSources, sourceId];
    onSourcesChange(newSelection);
  };

  return (
    <Box sx={{ display: 'grid', gap: 3, gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))' }}>
      {dataSources.map((source) => (
        <StyledCard
          key={source.id}
          className={selectedSources.includes(source.id) ? 'selected' : ''}
          onClick={() => handleSourceToggle(source.id)}
        >
          <StatusChip
            theme={theme}
            status={source.status}
            label={source.status === 'active' 
              ? 'Active' 
              : source.status === 'maintenance'
              ? 'Maintenance'
              : 'Limited'}
            size="small"
          />
          
          <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 2 }}>
            <Box sx={{ mr: 2, fontSize: '2rem' }}>{source.icon}</Box>
            <Box sx={{ flex: 1 }}>
              <Typography variant="h6" gutterBottom>
                {source.title}
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                {source.description}
              </Typography>
            </Box>
            <Checkbox
              checked={selectedSources.includes(source.id)}
              checkedIcon={<CheckCircleIcon />}
              sx={{ 
                color: theme.palette.primary.main,
                '&.Mui-checked': {
                  color: theme.palette.primary.main,
                },
              }}
            />
          </Box>

          <Box sx={{ mt: 'auto' }}>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <InfoIcon sx={{ fontSize: '1rem', mr: 0.5 }} />
              Avg. Response Time: {source.avgResponseTime}
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {source.capabilities.map((capability, index) => (
                <Tooltip key={index} title={capability}>
                  <Chip
                    label={capability}
                    size="small"
                    sx={{ 
                      backgroundColor: 'rgba(255, 107, 61, 0.1)',
                      color: theme.palette.primary.main,
                    }}
                  />
                </Tooltip>
              ))}
            </Box>
          </Box>
        </StyledCard>
      ))}
    </Box>
  );
};

export default DataSourceSelector; 