import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Typography,
  Box,
  Tabs,
  Tab,
} from '@mui/material';
import { transactions, books } from '../services/api';

function TabPanel({ children, value, index }) {
  return (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

function Transactions() {
  const [value, setValue] = useState(0);
  const [transactionsList, setTransactionsList] = useState([]);
  const [overdueTransactions, setOverdueTransactions] = useState([]);
  const [booksList, setBooksList] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [formData, setFormData] = useState({
    book: '',
    transaction_type: 'borrow',
    due_date: '',
  });

  useEffect(() => {
    fetchTransactions();
    fetchOverdueTransactions();
    fetchBooks();
  }, []);

  const fetchTransactions = async () => {
    try {
      const response = await transactions.getAll();
      setTransactionsList(response.data);
    } catch (error) {
      console.error('Error fetching transactions:', error);
    }
  };

  const fetchOverdueTransactions = async () => {
    try {
      const response = await transactions.getOverdue();
      setOverdueTransactions(response.data);
    } catch (error) {
      console.error('Error fetching overdue transactions:', error);
    }
  };

  const fetchBooks = async () => {
    try {
      const response = await books.getAll({ available: true });
      setBooksList(response.data);
    } catch (error) {
      console.error('Error fetching books:', error);
    }
  };

  const handleTabChange = (event, newValue) => {
    setValue(newValue);
  };

  const handleOpenDialog = () => {
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setFormData({
      book: '',
      transaction_type: 'borrow',
      due_date: '',
    });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await transactions.create(formData);
      handleCloseDialog();
      fetchTransactions();
      fetchOverdueTransactions();
      fetchBooks();
    } catch (error) {
      console.error('Error creating transaction:', error);
    }
  };

  const handleReturn = async (id) => {
    try {
      await transactions.update(id, { transaction_type: 'return' });
      fetchTransactions();
      fetchOverdueTransactions();
      fetchBooks();
    } catch (error) {
      console.error('Error returning book:', error);
    }
  };

  const renderTransactionTable = (transactions) => (
    <TableContainer>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Book</TableCell>
            <TableCell>User</TableCell>
            <TableCell>Type</TableCell>
            <TableCell>Transaction Date</TableCell>
            <TableCell>Due Date</TableCell>
            <TableCell>Return Date</TableCell>
            <TableCell>Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {transactions.map((transaction) => (
            <TableRow key={transaction.id}>
              <TableCell>{transaction.book_title}</TableCell>
              <TableCell>{transaction.user_username}</TableCell>
              <TableCell>{transaction.transaction_type}</TableCell>
              <TableCell>
                {new Date(transaction.transaction_date).toLocaleDateString()}
              </TableCell>
              <TableCell>
                {transaction.due_date &&
                  new Date(transaction.due_date).toLocaleDateString()}
              </TableCell>
              <TableCell>
                {transaction.return_date &&
                  new Date(transaction.return_date).toLocaleDateString()}
              </TableCell>
              <TableCell>
                {transaction.transaction_type === 'borrow' && (
                  <Button
                    color="primary"
                    onClick={() => handleReturn(transaction.id)}
                  >
                    Return
                  </Button>
                )}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Paper sx={{ p: 2 }}>
        <Typography variant="h5" gutterBottom>
          Transactions Management
        </Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={handleOpenDialog}
          sx={{ mb: 2 }}
        >
          New Transaction
        </Button>

        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={value} onChange={handleTabChange}>
            <Tab label="All Transactions" />
            <Tab label="Overdue Transactions" />
          </Tabs>
        </Box>

        <TabPanel value={value} index={0}>
          {renderTransactionTable(transactionsList)}
        </TabPanel>

        <TabPanel value={value} index={1}>
          {renderTransactionTable(overdueTransactions)}
        </TabPanel>
      </Paper>

      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>New Transaction</DialogTitle>
        <DialogContent>
          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              select
              label="Book"
              name="book"
              value={formData.book}
              onChange={handleChange}
              margin="normal"
              required
            >
              {booksList.map((book) => (
                <MenuItem key={book.id} value={book.id}>
                  {book.title}
                </MenuItem>
              ))}
            </TextField>
            <TextField
              fullWidth
              label="Due Date"
              name="due_date"
              type="date"
              value={formData.due_date}
              onChange={handleChange}
              margin="normal"
              required
              InputLabelProps={{
                shrink: true,
              }}
            />
          </form>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSubmit} color="primary">
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default Transactions;
