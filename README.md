# REG Application

## Project Overview
The **Regional Electricity Grid (REG) application** is a fault management system designed to handle electricity fault reports from clients, predict fault causes using AI, and efficiently assign the right technician for the job.

## Features
- **User Management**: Roles include Admins, Technicians, and Clients.
- **Problem Reportings**: The client submits his issue
- **Task Management**: Workflow for fault reporting, AI-based fault prediction, and technician assignment.
- **AI Fault Prediction**: Uses AI to analyze fault descriptions and suggest probable causes.
- **Grid Management**: Monitors electricity grids, status, and power allocation.

## Tech Stack
- **Backend**: Django, Django REST Framework
- **AI/ML**: Scikit-learn, Pandas
- **Database**: PostgreSQL (or SQLite for local development)

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- PostgreSQL (if using a production database)
- pip
- virtualenv

### Setup
1. **Clone the repository:**
   ```sh
 https://github.com/Nzamwitafab/ElectricDefaultDetectionBackend.git
  
   ```
2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Apply database migrations:**
   ```sh
   python manage.py migrate
   ```
5. **Create a superuser (optional, for admin access):**
   ```sh
   python manage.py createsuperuser
   ```
6. **Run the development server:**
   ```sh
   python manage.py runserver
   ```

## API Endpoints
### Authentication
- `POST /api/login/` - User login
- `POST /api/register/` - Register new users

### Task Management
- `POST /api/tasks/create/` - Create a new task
- `GET /api/tasks/` - Get all tasks
- `PATCH /api/tasks/<id>/update/` - Update task
- `DELETE /api/tasks/<id>/delete/` - Delete a task

### Grid Management
- `POST /api/grids/create/` - Create a new grid
- `GET /api/grids/` - List all grids
- `GET /api/grids/<id>/` - Get grid details
- `PATCH /api/grids/<id>/update/` - Update grid details
- `DELETE /api/grids/<id>/delete/` - Delete a grid


