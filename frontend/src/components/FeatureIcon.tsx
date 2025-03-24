import React from 'react';
import { Box, useTheme } from '@mui/material';

interface FeatureIconProps {
  icon: string;
}

const FeatureIcon: React.FC<FeatureIconProps> = ({ icon }) => {
  const theme = useTheme();

  return (
    <Box
      sx={{
        width: 80,
        height: 80,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        borderRadius: '20px',
        backgroundColor: 'rgba(255, 107, 61, 0.1)',
        fontSize: '2.5rem',
        marginBottom: theme.spacing(3),
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'scale(1.1)',
          backgroundColor: 'rgba(255, 107, 61, 0.15)',
        },
      }}
    >
      {icon}
    </Box>
  );
};

export default FeatureIcon; 