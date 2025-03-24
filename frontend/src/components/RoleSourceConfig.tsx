import React, { useState, useEffect } from 'react';
import {
  Box,
  Chip,
  Typography,
  TextField,
  Autocomplete,
  CircularProgress,
  Paper,
  Divider,
  Button,
  Alert,
} from '@mui/material';
import { useDataSources } from '../contexts/DataSourceContext';
import { dataSourceService, RoleCategory } from '../services/dataSourceService';

interface RoleSourceConfigProps {
  onConfigured: () => void;
}

const RoleSourceConfig: React.FC<RoleSourceConfigProps> = ({ onConfigured }) => {
  const { updateSourceConfig } = useDataSources();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [roleCategories, setRoleCategories] = useState<RoleCategory[]>([]);
  const [selectedRoles, setSelectedRoles] = useState<string[]>([]);
  const [popularRoles, setPopularRoles] = useState<string[]>([]);
  const [searchInput, setSearchInput] = useState('');
  const [searchResults, setSearchResults] = useState<string[]>([]);

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const [categories, popular] = await Promise.all([
          dataSourceService.getRoleCategories(),
          dataSourceService.getPopularRoles(),
        ]);
        setRoleCategories(categories);
        setPopularRoles(popular);
      } catch (err) {
        setError('Failed to load role data');
      }
    };

    fetchInitialData();
  }, []);

  useEffect(() => {
    const searchRoles = async () => {
      if (searchInput.trim().length > 2) {
        try {
          const results = await dataSourceService.searchRoles(searchInput);
          setSearchResults(results);
        } catch (err) {
          console.error('Failed to search roles:', err);
        }
      }
    };

    const timeoutId = setTimeout(searchRoles, 300);
    return () => clearTimeout(timeoutId);
  }, [searchInput]);

  const handleRoleSelect = (role: string) => {
    if (!selectedRoles.includes(role)) {
      setSelectedRoles([...selectedRoles, role]);
    }
  };

  const handleRoleRemove = (role: string) => {
    setSelectedRoles(selectedRoles.filter(r => r !== role));
  };

  const handleSave = async () => {
    setLoading(true);
    setError(null);

    try {
      // Get stats for selected roles
      const stats = await dataSourceService.getRoleStats(selectedRoles);

      // Update the role-based source configuration
      await updateSourceConfig('role-based', {
        status: 'configured',
        filters: {
          roles: selectedRoles,
        },
      });

      onConfigured();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to configure role targeting');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Configure Role-Based Targeting
      </Typography>
      <Divider sx={{ my: 2 }} />

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Box sx={{ mb: 4 }}>
        <Typography variant="subtitle1" gutterBottom>
          Search and select target roles
        </Typography>
        <Autocomplete
          multiple
          options={searchResults}
          value={selectedRoles}
          onChange={(_, newValue) => setSelectedRoles(newValue)}
          inputValue={searchInput}
          onInputChange={(_, newInput) => setSearchInput(newInput)}
          renderInput={(params) => (
            <TextField
              {...params}
              variant="outlined"
              placeholder="Search roles..."
              fullWidth
            />
          )}
          renderTags={(value, getTagProps) =>
            value.map((role, index) => (
              <Chip
                {...getTagProps({ index })}
                key={role}
                label={role}
                onDelete={() => handleRoleRemove(role)}
              />
            ))
          }
        />
      </Box>

      <Box sx={{ mb: 4 }}>
        <Typography variant="subtitle1" gutterBottom>
          Popular Roles
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {popularRoles.map((role) => (
            <Chip
              key={role}
              label={role}
              onClick={() => handleRoleSelect(role)}
              sx={{
                cursor: 'pointer',
                opacity: selectedRoles.includes(role) ? 0.6 : 1,
              }}
            />
          ))}
        </Box>
      </Box>

      <Box sx={{ mb: 4 }}>
        <Typography variant="subtitle1" gutterBottom>
          Role Categories
        </Typography>
        {roleCategories.map((category) => (
          <Box key={category.id} sx={{ mb: 2 }}>
            <Typography variant="subtitle2" gutterBottom>
              {category.name}
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {category.roles.map((role) => (
                <Chip
                  key={role}
                  label={role}
                  onClick={() => handleRoleSelect(role)}
                  sx={{
                    cursor: 'pointer',
                    opacity: selectedRoles.includes(role) ? 0.6 : 1,
                  }}
                />
              ))}
            </Box>
          </Box>
        ))}
      </Box>

      <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
        {loading && <CircularProgress size={24} />}
        <Button
          variant="contained"
          onClick={handleSave}
          disabled={loading || selectedRoles.length === 0}
        >
          Save Role Configuration
        </Button>
      </Box>
    </Paper>
  );
};

export default RoleSourceConfig; 