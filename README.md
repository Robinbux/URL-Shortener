# URL Shortener Service

This project is a URL shortener service built with FastAPI, SQLAlchemy, and PostgreSQL. It allows users to create shortened URLs that redirect to the original URLs and provides basic statistics about the usage of these shortened URLs.

## Features

- **Shorten URLs**: Convert long URLs into short, manageable links that redirect to the original URLs.
- **Redirect**: Use the short URL to redirect to the original URL.
- **Statistics**: View how often a shortened URL has been used.

## Requirements

Use a modern Python version (tested with Python 3.11) and install the required packages with pip:

```bash
pip install -r requirements.txt
```

## Installation

First, clone the repository:

```bash
git clone https://github.com/your-username/url-shortener.git
cd url-shortener
```
Install the required packages:

```bash
pip install -r requirements.txt
```

## Database Setup

Ensure that PostgreSQL is installed and running on your machine. Create a new database for the application:

```sql
CREATE DATABASE url_shortener;
```
Create a user and grant privileges:

```sql
CREATE USER urlshortener_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE url_shortener TO urlshortener_user;
```

## Configuration

Create a .env file in the root directory with the following contents, replacing the values with your database details:

```
DB_USER=urlshortener_user
DB_PASS=your_password
DB_NAME=url_shortener
DB_HOST=localhost
```

## Running the Application

Start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

## Testing the Application

To test the application, use the interactive API documentation at http://localhost:8000/docs, or use tools like curl, HTTPie, or Postman to send requests to the API endpoints.

## Automated Testing

Run the automated tests with pytest:

```bash
pytest -v
```