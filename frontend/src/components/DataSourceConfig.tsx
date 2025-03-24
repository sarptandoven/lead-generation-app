import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Alert,
  CircularProgress,
  Stepper,
  Step,
  StepLabel,
  Paper,
  Divider,
  Chip,
} from '@mui/material';
import { useDataSources } from '../contexts/DataSourceContext';
import { dataSourceService } from '../services/dataSourceService';
import RoleSourceConfig from './RoleSourceConfig';

interface DataSourceConfigProps {
  sourceId: string;
  onConfigured: () => void;
}

const sourceRequirements = {
  linkedin: {
    steps: ['API Credentials', 'Rate Limits', 'Filters'],
    fields: {
      clientId: 'Client ID',
      clientSecret: 'Client Secret',
      refreshToken: 'Refresh Token',
    },
  },
  google: {
    steps: ['API Key', 'Location Settings', 'Filters'],
    fields: {
      apiKey: 'API Key',
    },
  },
  bing: {
    steps: ['API Key', 'Search Settings', 'Filters'],
    fields: {
      apiKey: 'API Key',
    },
  },
  'yellow-pages': {
    steps: ['Access Token', 'Location Settings', 'Filters'],
    fields: {
      apiKey: 'Access Token',
    },
  },
  crunchbase: {
    steps: ['API Key', 'Data Settings', 'Filters'],
    fields: {
      apiKey: 'API Key',
      userKey: 'User Key',
    },
  },
  'role-based': {
    steps: ['Role Selection', 'Filters'],
    fields: {},
  },
};

const DataSourceConfig: React.FC<DataSourceConfigProps> = ({ sourceId, onConfigured }) => {
  const { sourceConfigs, updateSourceConfig } = useDataSources();
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState<Record<string, string>>({});

  const requirements = sourceRequirements[sourceId as keyof typeof sourceRequirements];

  const handleInputChange = (field: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [field]: event.target.value,
    }));
  };

  const handleNext = async () => {
    if (activeStep === requirements.steps.length - 1) {
      await handleSubmit();
    } else {
      setActiveStep(prev => prev + 1);
    }
  };

  const handleBack = () => {
    setActiveStep(prev => prev - 1);
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);

    try {
      // Configure the source
      const config = await dataSourceService.configureSource(sourceId, {
        credentials: formData,
        status: 'configuring',
      });

      // Test the connection
      const testResult = await dataSourceService.testSourceConnection(sourceId);

      if (testResult.success) {
        updateSourceConfig(sourceId, {
          ...config,
          status: 'configured',
        });
        onConfigured();
      } else {
        throw new Error(testResult.error || 'Failed to connect to the data source');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      updateSourceConfig(sourceId, {
        status: 'error',
        error: err instanceof Error ? err.message : 'An error occurred',
      });
    } finally {
      setLoading(false);
    }
  };

  const renderStepContent = (step: number) => {
    if (sourceId === 'role-based') {
      return <RoleSourceConfig onConfigured={onConfigured} />;
    }

    switch (step) {
      case 0:
        return (
          <Box sx={{ mt: 2 }}>
            {Object.entries(requirements.fields).map(([field, label]) => (
              <TextField
                key={field}
                fullWidth
                label={label}
                variant="outlined"
                margin="normal"
                value={formData[field] || ''}
                onChange={handleInputChange(field)}
                type="password"
              />
            ))}
          </Box>
        );
      case 1:
        return (
          <Box sx={{ mt: 2 }}>
            <Typography variant="body1" gutterBottom>
              Configure rate limits and access settings for {sourceId}
            </Typography>
            {/* Add rate limit and access settings fields here */}
          </Box>
        );
      case 2:
        return (
          <Box sx={{ mt: 2 }}>
            <Typography variant="body1" gutterBottom>
              Set up filters for the type of leads you want to collect
            </Typography>
            {/* Add filter configuration fields here */}
          </Box>
        );
      default:
        return null;
    }
  };

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Configure {sourceId.charAt(0).toUpperCase() + sourceId.slice(1)}
      </Typography>
      <Divider sx={{ my: 2 }} />

      <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
        {requirements.steps.map((label, index) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {renderStepContent(activeStep)}

      <Box sx={{ mt: 4, display: 'flex', justifyContent: 'space-between' }}>
        <Button
          disabled={activeStep === 0 || loading}
          onClick={handleBack}
        >
          Back
        </Button>
        <Box sx={{ display: 'flex', gap: 2 }}>
          {loading && <CircularProgress size={24} sx={{ mr: 1 }} />}
          <Button
            variant="contained"
            onClick={handleNext}
            disabled={loading}
          >
            {activeStep === requirements.steps.length - 1 ? 'Finish' : 'Next'}
          </Button>
        </Box>
      </Box>

      {sourceConfigs[sourceId]?.status === 'configured' && (
        <Chip
          label="Configured"
          color="success"
          sx={{ mt: 2 }}
        />
      )}
    </Paper>
  );
};

export default DataSourceConfig; 