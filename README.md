# Lucid Task Submission

## Overview
This is a FastAPI application implementing a simple blog system with user authentication and post management. It follows the MVC pattern with SQLAlchemy for ORM and Pydantic for validation.

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/WinChester1723/lucid-task.git
   cd lucid-task

## Notes
- The application uses SQLite (`lucid_task.db`) for development purposes. For production, it can be adapted to MySQL by updating `src/models/database.py` with the appropriate connection string.