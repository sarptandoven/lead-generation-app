import React, { useState } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  TextField,
  Switch,
  FormControlLabel,
  Button,
  Box,
} from '@mui/material';

interface Settings {
  emailNotifications: boolean;
  leadScoreThreshold: number;
  autoAssignment: boolean;
  apiKey: string;
}

const Settings: React.FC = () => {
  const [settings, setSettings] = useState<Settings>({
    emailNotifications: true,
    leadScoreThreshold: 70,
    autoAssignment: false,
    apiKey: '********-****-****-****-************',
  });

  const handleChange = (field: keyof Settings) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const value = event.target.type === 'checkbox' 
      ? event.target.checked 
      : event.target.value;
    
    setSettings((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSave = () => {
    console.log('Saving settings:', settings);
    // Implement API call to save settings
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Settings
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Notifications
              </Typography>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.emailNotifications}
                    onChange={handleChange('emailNotifications')}
                  />
                }
                label="Email Notifications"
              />
              <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                Receive email notifications for new leads and updates
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Lead Scoring
              </Typography>
              <TextField
                fullWidth
                label="Lead Score Threshold"
                type="number"
                value={settings.leadScoreThreshold}
                onChange={handleChange('leadScoreThreshold')}
                helperText="Minimum score for lead qualification"
                sx={{ mb: 2 }}
              />
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.autoAssignment}
                    onChange={handleChange('autoAssignment')}
                  />
                }
                label="Automatic Lead Assignment"
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                API Configuration
              </Typography>
              <TextField
                fullWidth
                label="API Key"
                type="password"
                value={settings.apiKey}
                onChange={handleChange('apiKey')}
                sx={{ mb: 2 }}
              />
              <Typography variant="body2" color="textSecondary">
                Your API key for external integrations
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          variant="contained"
          color="primary"
          onClick={handleSave}
        >
          Save Changes
        </Button>
      </Box>
    </Container>
  );
};

export default Settings; 