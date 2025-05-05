# Employer Management System

A simple Employer Management System API built using Django REST Framework with custom authentication and CRUD operations for Employers.

## Overview

This API allows users to register, login, and manage their employers. The system uses a custom User model and JWT-based authentication. Each user can create, view, update, and delete their associated employers.

## Features

- Custom User Authentication (extends AbstractBaseUser)
- JWT-based authentication
- Email-based login (instead of username)
- CRUD operations for Employers
- User-specific employer management (users can only access their own employers)
- Interactive API documentation with Swagger and ReDoc

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup/` | Register a new user |
| POST | `/api/auth/login/` | Login and get JWT tokens |
| GET | `/api/auth/profile/` | Get logged-in user's profile |
| POST | `/api/employers/` | Create an Employer |
| GET | `/api/employers/` | List all Employers for the logged-in user |
| GET | `/api/employers/<id>/` | Retrieve a specific Employer |
| PUT | `/api/employers/<id>/` | Update a specific Employer |
| DELETE | `/api/employers/<id>/` | Delete a specific Employer |

## API Documentation

The API includes interactive documentation:

- **Swagger UI**: Access at `/api/docs/` for an interactive documentation interface
- **ReDoc**: Access at `/api/redoc/` for a responsive, easy-to-navigate API reference

These documentation paths provide:
- Detailed information on all endpoints
- Request/response examples
- Authentication requirements
- Schema models
- Try-it-out functionality (in Swagger UI)

## Models

### User Model

Custom User model that extends AbstractBaseUser and PermissionsMixin with:
- Email-based authentication
- Required fields: email, name
- Login with email and password

### Employer Model

Represents an employer with the following fields:
- id (AutoField)
- company_name (CharField)
- contact_person_name (CharField)
- email (EmailField)
- phone_number (CharField)
- address (TextField)
- created_at (DateTimeField, auto_now_add=True)
- Linked to a User via ForeignKey (User can have multiple Employers)

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Django 5.2
- Django REST Framework
- Simple JWT

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd Softvence
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv ems
   source ems/Scripts/activate  # On Windows: .\ems\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Environment Configuration:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file to configure your environment variables, especially:
   - Set a strong SECRET_KEY
   - Set DEBUG=True for development

5. Apply migrations:
   ```
   python manage.py migrate
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

The API will be available at http://127.0.0.1:8000/

## Environment Variables

The project uses environment variables for configuration. An example file (`.env.example`) is provided as a template. To set up your environment:

1. Copy `.env.example` to `.env`
2. Update the values according to your needs

Important variables:
- `SECRET_KEY`: Django's secret key (critical for security)
- `DEBUG`: Set to "True" for development, "False" for production
- Other optional variables for database configuration, allowed hosts, etc.

## Authentication

This system uses JWT (JSON Web Token) for authentication. To access protected endpoints:

1. Register a user at `/api/auth/signup/`
2. Obtain JWT tokens by logging in at `/api/auth/login/`
3. Include the access token in the Authorization header for subsequent requests:
   ```
   Authorization: Bearer <your_access_token>
   ```

## Permissions

- Only authenticated users can access employer endpoints
- Users can only access, update, or delete their own employers

## Technologies Used

- Django
- Django REST Framework
- Simple JWT for authentication
- python-dotenv for environment variable management
- SQLite (development database)
- drf-yasg for Swagger/ReDoc documentation