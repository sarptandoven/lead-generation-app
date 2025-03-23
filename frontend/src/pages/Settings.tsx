import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  TextField,
  Button,
  Switch,
  FormControlLabel,
  Divider,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  CardActions,
} from '@mui/material';

interface Settings {
  linkedin: {
    enabled: boolean;
    username: string;
    password: string;
    maxLeadsPerSearch: number;
  };
  airbnb: {
    enabled: boolean;
    maxListingsPerSearch: number;
    minPrice: number;
    maxPrice: number;
  };
  web: {
    enabled: boolean;
    maxResultsPerQuery: number;
    excludedDomains: string[];
  };
  notifications: {
    email: boolean;
    slack: boolean;
    webhook: boolean;
    webhookUrl: string;
  };
  ai: {
    enabled: boolean;
    model: string;
    confidenceThreshold: number;
  };
}

const Settings: React.FC = () => {
  const [settings, setSettings] = useState<Settings>({
    linkedin: {
      enabled: false,
      username: '',
      password: '',
      maxLeadsPerSearch: 100,
    },
    airbnb: {
      enabled: false,
      maxListingsPerSearch: 50,
      minPrice: 0,
      maxPrice: 1000,
    },
    web: {
      enabled: false,
      maxResultsPerQuery: 20,
      excludedDomains: [],
    },
    notifications: {
      email: true,
      slack: false,
      webhook: false,
      webhookUrl: '',
    },
    ai: {
      enabled: true,
      model: 'gpt-4',
      confidenceThreshold: 0.8,
    },
  });
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/settings', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });
      if (!response.ok) {
        throw new Error('Failed to fetch settings');
      }
      const data = await response.json();
      setSettings(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch('http://localhost:8000/settings', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify(settings),
      });

      if (!response.ok) {
        throw new Error('Failed to save settings');
      }

      setSuccess('Settings saved successfully');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setSaving(false);
    }
  };

  const handleChange = (section: keyof Settings, field: string, value: any) => {
    setSettings(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value,
      },
    }));
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {success}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* LinkedIn Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                LinkedIn Settings
              </Typography>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.linkedin.enabled}
                    onChange={(e) => handleChange('linkedin', 'enabled', e.target.checked)}
                  />
                }
                label="Enable LinkedIn Scraping"
              />
              <TextField
                fullWidth
                label="Username"
                value={settings.linkedin.username}
                onChange={(e) => handleChange('linkedin', 'username', e.target.value)}
                margin="normal"
                disabled={!settings.linkedin.enabled}
              />
              <TextField
                fullWidth
                label="Password"
                type="password"
                value={settings.linkedin.password}
                onChange={(e) => handleChange('linkedin', 'password', e.target.value)}
                margin="normal"
                disabled={!settings.linkedin.enabled}
              />
              <TextField
                fullWidth
                label="Max Leads Per Search"
                type="number"
                value={settings.linkedin.maxLeadsPerSearch}
                onChange={(e) => handleChange('linkedin', 'maxLeadsPerSearch', parseInt(e.target.value))}
                margin="normal"
                disabled={!settings.linkedin.enabled}
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Airbnb Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Airbnb Settings
              </Typography>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.airbnb.enabled}
                    onChange={(e) => handleChange('airbnb', 'enabled', e.target.checked)}
                  />
                }
                label="Enable Airbnb Scraping"
              />
              <TextField
                fullWidth
                label="Max Listings Per Search"
                type="number"
                value={settings.airbnb.maxListingsPerSearch}
                onChange={(e) => handleChange('airbnb', 'maxListingsPerSearch', parseInt(e.target.value))}
                margin="normal"
                disabled={!settings.airbnb.enabled}
              />
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Min Price"
                    type="number"
                    value={settings.airbnb.minPrice}
                    onChange={(e) => handleChange('airbnb', 'minPrice', parseInt(e.target.value))}
                    margin="normal"
                    disabled={!settings.airbnb.enabled}
                  />
                </Grid>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Max Price"
                    type="number"
                    value={settings.airbnb.maxPrice}
                    onChange={(e) => handleChange('airbnb', 'maxPrice', parseInt(e.target.value))}
                    margin="normal"
                    disabled={!settings.airbnb.enabled}
                  />
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Web Scraping Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Web Scraping Settings
              </Typography>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.web.enabled}
                    onChange={(e) => handleChange('web', 'enabled', e.target.checked)}
                  />
                }
                label="Enable Web Scraping"
              />
              <TextField
                fullWidth
                label="Max Results Per Query"
                type="number"
                value={settings.web.maxResultsPerQuery}
                onChange={(e) => handleChange('web', 'maxResultsPerQuery', parseInt(e.target.value))}
                margin="normal"
                disabled={!settings.web.enabled}
              />
              <TextField
                fullWidth
                label="Excluded Domains (comma-separated)"
                value={settings.web.excludedDomains.join(', ')}
                onChange={(e) => handleChange('web', 'excludedDomains', e.target.value.split(',').map(d => d.trim()))}
                margin="normal"
                disabled={!settings.web.enabled}
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Notification Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Notification Settings
              </Typography>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.notifications.email}
                    onChange={(e) => handleChange('notifications', 'email', e.target.checked)}
                  />
                }
                label="Email Notifications"
              />
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.notifications.slack}
                    onChange={(e) => handleChange('notifications', 'slack', e.target.checked)}
                  />
                }
                label="Slack Notifications"
              />
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.notifications.webhook}
                    onChange={(e) => handleChange('notifications', 'webhook', e.target.checked)}
                  />
                }
                label="Webhook Notifications"
              />
              <TextField
                fullWidth
                label="Webhook URL"
                value={settings.notifications.webhookUrl}
                onChange={(e) => handleChange('notifications', 'webhookUrl', e.target.value)}
                margin="normal"
                disabled={!settings.notifications.webhook}
              />
            </CardContent>
          </Card>
        </Grid>

        {/* AI Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                AI Settings
              </Typography>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.ai.enabled}
                    onChange={(e) => handleChange('ai', 'enabled', e.target.checked)}
                  />
                }
                label="Enable AI Lead Scoring"
              />
              <TextField
                fullWidth
                label="AI Model"
                value={settings.ai.model}
                onChange={(e) => handleChange('ai', 'model', e.target.value)}
                margin="normal"
                disabled={!settings.ai.enabled}
              />
              <TextField
                fullWidth
                label="Confidence Threshold"
                type="number"
                value={settings.ai.confidenceThreshold}
                onChange={(e) => handleChange('ai', 'confidenceThreshold', parseFloat(e.target.value))}
                margin="normal"
                disabled={!settings.ai.enabled}
                inputProps={{ min: 0, max: 1, step: 0.1 }}
              />
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          variant="contained"
          onClick={handleSave}
          disabled={saving}
        >
          {saving ? <CircularProgress size={24} /> : 'Save Settings'}
        </Button>
      </Box>
    </Box>
  );
};

export default Settings; 