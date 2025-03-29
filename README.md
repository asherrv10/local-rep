# College Event Management System

A simple desktop application built with Python and Tkinter that allows college administrators and students to manage events with role-based access control.

## Features

- **User Authentication System**
  - Registration and login functionality
  - Role-based access (admin/student)

- **Event Management**
  - Create events (available to all users)
  - View all events with detailed information
  - Edit events (admin only)
  - Delete events (admin only)

- **Database Integration**
  - SQLite database to store user information and event details
  - Persistent data storage

## Requirements

- Python 3.6 or higher
- Tkinter (usually comes pre-installed with Python)
- SQLite3 (included in Python standard library)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/asherrv10/college-event-management.git
   cd college-event-management
   ```

2. Run the application:
   ```
   python clg.py
   ```

## Usage Guide

### Registration

1. Launch the application
2. Click on the "Register" button
3. Enter your desired username, password, and role (admin/student)
4. Click "OK" to complete registration

### Login

1. Enter your username and password
2. Click "Login"
3. Upon successful login, you'll be redirected to the Event Dashboard

### Creating Events (All Users)

1. From the Event Dashboard, click "Create New Event"
2. Fill in all required fields:
   - Event Name
   - Description
   - Organizer
   - Date
3. Click "Save Event"

### Admin-Only Functions

If logged in as an admin user:

- **Editing Events**:
  1. Select an event from the list
  2. Click "Edit Event"
  3. Modify details as needed
  4. Click "Save Changes"

- **Deleting Events**:
  1. Select an event from the list
  2. Click "Delete Event"
  3. Confirm deletion

## Database Structure

The application uses two main tables:

1. **users**
   - username (Primary Key)
   - password
   - role

2. **events**
   - event_id (Primary Key, Autoincrement)
   - event_name
   - description
   - date
   - organizer
   - created_by

## Screenshots

![Capture](https://github.com/user-attachments/assets/0f8da7f6-6d9a-4c67-8db1-0b18cd09c28b)
![Capture-2](https://github.com/user-attachments/assets/af780d10-b665-4c4e-a238-49c7eecdaee0)
![Capture-3](https://github.com/user-attachments/assets/5e299833-b25b-447e-9aab-482bbd72c874)


## Future Enhancements

- Password encryption
- Event search functionality
- Event registration for students
- Email notifications
- Improved UI with themes

## License

[MIT License](LICENSE)

## Contributors

- asher

## Acknowledgments

- Claude AI for the support
