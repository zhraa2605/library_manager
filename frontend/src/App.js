import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { createTheme } from '@mui/material/styles';
import Navbar from './components/Navbar';
import Books from './components/Books';
import Categories from './components/Categories';
import Transactions from './components/Transactions';
import Login from './components/Login';
import Register from './components/Register';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  const [isAuthenticated, setIsAuthenticated] = React.useState(
    !!localStorage.getItem('token')
  );

  const handleLogin = (token) => {
    localStorage.setItem('token', token);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Navbar isAuthenticated={isAuthenticated} onLogout={handleLogout} />
        <Routes>
          <Route
            path="/"
            element={
              isAuthenticated ? (
                <Navigate to="/books" />
              ) : (
                <Navigate to="/login" />
              )
            }
          />
          <Route
            path="/login"
            element={
              !isAuthenticated ? (
                <Login onLogin={handleLogin} />
              ) : (
                <Navigate to="/books" />
              )
            }
          />
          <Route
            path="/register"
            element={
              !isAuthenticated ? (
                <Register onLogin={handleLogin} />
              ) : (
                <Navigate to="/books" />
              )
            }
          />
          <Route
            path="/books"
            element={
              isAuthenticated ? <Books /> : <Navigate to="/login" />
            }
          />
          <Route
            path="/categories"
            element={
              isAuthenticated ? <Categories /> : <Navigate to="/login" />
            }
          />
          <Route
            path="/transactions"
            element={
              isAuthenticated ? <Transactions /> : <Navigate to="/login" />
            }
          />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
