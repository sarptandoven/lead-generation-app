import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Menu,
  MenuItem,
  Box,
} from '@mui/material';
import {
  AccountCircle,
  Dashboard as DashboardIcon,
  Group as GroupIcon,
  Settings as SettingsIcon,
  Add as AddIcon,
} from '@mui/icons-material';

const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleNavigate = (path: string) => {
    navigate(path);
    handleClose();
  };

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Lead Generation App
        </Typography>
        
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <IconButton
            color={isActive('/dashboard') ? 'secondary' : 'inherit'}
            onClick={() => handleNavigate('/dashboard')}
          >
            <DashboardIcon />
          </IconButton>
          
          <IconButton
            color={isActive('/lead-generation') ? 'secondary' : 'inherit'}
            onClick={() => handleNavigate('/lead-generation')}
          >
            <AddIcon />
          </IconButton>
          
          <IconButton
            color={isActive('/lead-management') ? 'secondary' : 'inherit'}
            onClick={() => handleNavigate('/lead-management')}
          >
            <GroupIcon />
          </IconButton>
          
          <IconButton
            color={isActive('/settings') ? 'secondary' : 'inherit'}
            onClick={() => handleNavigate('/settings')}
          >
            <SettingsIcon />
          </IconButton>
          
          <IconButton
            onClick={handleMenu}
            color="inherit"
          >
            <AccountCircle />
          </IconButton>
        </Box>
        
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleClose}
        >
          <MenuItem onClick={() => handleNavigate('/profile')}>Profile</MenuItem>
          <MenuItem onClick={() => handleNavigate('/logout')}>Logout</MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar; 