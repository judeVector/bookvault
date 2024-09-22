# BookVault

**BookVault** is a library management service built with Django REST Framework (DRF) that allows users to browse a catalogue of books and borrow them. It consists of two independent API services for users and admins.

## Features

### Frontend API (User Facing)

- **Enroll users**: Users can register with their email, first name, and last name.
- **Browse catalogue**: List all available books in the library.
- **Book details**: View detailed information about a book by its ID.
- **Filter books**: Filter books by publisher (e.g., Wiley, Apress, Manning) or by category (e.g., fiction, technology, science).
- **Borrow books**: Users can borrow a book by specifying the borrowing duration in days.

### Admin API

- **Add new books**: Admins can add new books to the library catalogue.
- **Remove books**: Admins can remove books from the catalogue.
- **View users**: Fetch and list all users enrolled in the library.
- **View borrowed books**: Admins can see which users have borrowed books and when the books will be available again.
- **Unavailable books**: List books that are currently unavailable for borrowing, with their expected availability date.

## Tech Stack

- **Backend**: Django REST Framework (DRF)
- **Data Stores**: SQLiteDB (other DB solutions can be utilized if needed)
- **Containerization**: Docker for both services
- **Testing**: Unit and integration tests for service validation
- **Messaging Queue**: Used RabbitMQ for communication between the two services

## Architecture

BookVault is built with two independent services:

1. **Frontend API**: Handles user interactions like book browsing, registration, and borrowing.
2. **Backend/Admin API**: Manages library operations such as book cataloging and user management.
