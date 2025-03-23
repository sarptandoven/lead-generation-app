import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  CardActions,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { format } from 'date-fns';
import { SelectChangeEvent } from '@mui/material/Select';

interface Lead {
  name: string;
  title: string;
  company: string;
  location: string;
  email?: string;
  phone?: string;
  source: string;
  score?: number;
}

const LeadGeneration: React.FC = () => {
  const [source, setSource] = useState<string>('');
  const [location, setLocation] = useState<string>('');
  const [industries, setIndustries] = useState<string[]>([]);
  const [startDate, setStartDate] = useState<Date | null>(null);
  const [endDate, setEndDate] = useState<Date | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [leads, setLeads] = useState<Lead[]>([]);
  const [progress, setProgress] = useState<number>(0);

  const handleSourceChange = (event: SelectChangeEvent<string>) => {
    setSource(event.target.value);
  };

  const handleIndustryAdd = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter' && event.currentTarget.value) {
      setIndustries([...industries, event.currentTarget.value]);
      event.currentTarget.value = '';
    }
  };

  const handleIndustryDelete = (industryToDelete: string) => {
    setIndustries(industries.filter((industry) => industry !== industryToDelete));
  };

  const handleGenerate = async () => {
    setLoading(true);
    setError('');
    setProgress(0);
    setLeads([]);

    try {
      const response = await fetch('http://localhost:8000/scrape', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          source,
          parameters: {
            location,
            industries,
            start_date: startDate ? format(startDate, 'yyyy-MM-dd') : undefined,
            end_date: endDate ? format(endDate, 'yyyy-MM-dd') : undefined,
          },
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate leads');
      }

      const data = await response.json();
      setLeads(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
      setProgress(100);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Generate Leads
      </Typography>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Source</InputLabel>
              <Select
                value={source}
                label="Source"
                onChange={handleSourceChange}
              >
                <MenuItem value="linkedin">LinkedIn</MenuItem>
                <MenuItem value="airbnb">Airbnb</MenuItem>
                <MenuItem value="web">Web Search</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Location"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            />
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Industries (Press Enter to add)"
              onKeyPress={handleIndustryAdd}
            />
            <Box sx={{ mt: 1, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {industries.map((industry) => (
                <Chip
                  key={industry}
                  label={industry}
                  onDelete={() => handleIndustryDelete(industry)}
                />
              ))}
            </Box>
          </Grid>

          <Grid item xs={12} md={6}>
            <LocalizationProvider dateAdapter={AdapterDateFns}>
              <DatePicker
                label="Start Date"
                value={startDate}
                onChange={setStartDate}
                slotProps={{ textField: { fullWidth: true } }}
              />
            </LocalizationProvider>
          </Grid>

          <Grid item xs={12} md={6}>
            <LocalizationProvider dateAdapter={AdapterDateFns}>
              <DatePicker
                label="End Date"
                value={endDate}
                onChange={setEndDate}
                slotProps={{ textField: { fullWidth: true } }}
              />
            </LocalizationProvider>
          </Grid>

          <Grid item xs={12}>
            <Button
              variant="contained"
              onClick={handleGenerate}
              disabled={loading || !source}
              fullWidth
            >
              {loading ? <CircularProgress size={24} /> : 'Generate Leads'}
            </Button>
          </Grid>

          {error && (
            <Grid item xs={12}>
              <Alert severity="error">{error}</Alert>
            </Grid>
          )}

          {loading && (
            <Grid item xs={12}>
              <CircularProgress variant="determinate" value={progress} />
            </Grid>
          )}
        </Grid>
      </Paper>

      {leads.length > 0 && (
        <Typography variant="h5" gutterBottom>
          Generated Leads
        </Typography>
      )}

      <Grid container spacing={2}>
        {leads.map((lead, index) => (
          <Grid item xs={12} md={6} lg={4} key={index}>
            <Card>
              <CardContent>
                <Typography variant="h6">{lead.name}</Typography>
                <Typography color="textSecondary" gutterBottom>
                  {lead.title}
                </Typography>
                <Typography variant="body2" gutterBottom>
                  {lead.company}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  {lead.location}
                </Typography>
                {lead.email && (
                  <Typography variant="body2">{lead.email}</Typography>
                )}
                {lead.phone && (
                  <Typography variant="body2">{lead.phone}</Typography>
                )}
                <Chip
                  label={lead.source}
                  size="small"
                  sx={{ mt: 1 }}
                />
                {lead.score && (
                  <Typography variant="body2" color="primary" sx={{ mt: 1 }}>
                    Score: {lead.score}
                  </Typography>
                )}
              </CardContent>
              <CardActions>
                <Button size="small">View Details</Button>
                <Button size="small">Add to CRM</Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default LeadGeneration; 