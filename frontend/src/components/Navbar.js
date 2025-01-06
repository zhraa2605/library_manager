import React from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
} from '@mui/material';
import { auth } from '../services/api';

function Navbar({ isAuthenticated, onLogout }) {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await auth.logout();
      onLogout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Library Manager
        </Typography>
        {isAuthenticated ? (
          <Box>
            <Button
              color="inherit"
              component={RouterLink}
              to="/books"
            >
              Books
            </Button>
            <Button
              color="inherit"
              component={RouterLink}
              to="/categories"
            >
              Categories
            </Button>
            <Button
              color="inherit"
              component={RouterLink}
              to="/transactions"
            >
              Transactions
            </Button>
            <Button color="inherit" onClick={handleLogout}>
              Logout
            </Button>
          </Box>
        ) : (
          <Box>
            <Button
              color="inherit"
              component={RouterLink}
              to="/login"
            >
              Login
            </Button>
            <Button
              color="inherit"
              component={RouterLink}
              to="/register"
            >
              Register
            </Button>
          </Box>
        )}
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
