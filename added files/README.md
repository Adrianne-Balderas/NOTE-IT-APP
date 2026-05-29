# NOTE-IT-APP (Flask REST API Enhancement)

## Project Description

This project is a Flask-based note-taking web application enhanced with
a REST API using Flask-RESTX.\
It includes full CRUD functionality, Swagger documentation,
authentication, and unit testing.

------------------------------------------------------------------------

## Features

-   Create, Read, Update, Delete (CRUD) Notes
-   User authentication (Login/Register)
-   Public & Private notes
-   REST API using Flask-RESTX
-   Swagger UI documentation
-   Unit testing with pytest
-   SQLite database support

------------------------------------------------------------------------

## Tech Stack

-   Flask
-   Flask-SQLAlchemy
-   Flask-Login
-   Flask-RESTX (Swagger)
-   Pytest
-   SQLite

------------------------------------------------------------------------

## API Documentation (Swagger)

After running the project, open:

http://127.0.0.1:5000/docs

------------------------------------------------------------------------

## Installation Guide

### 1. Clone the repository

git clone https://github.com/Adrianne-Balderas/NOTE-IT-APP

### 2. Create virtual environment

python -m venv venv venv`\Scripts`{=tex}`\activate   `{=tex}(Windows)

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run the app

python main.py

------------------------------------------------------------------------

## API Endpoints

### Notes API

-   GET /api/notes/ → Get all notes
-   POST /api/notes/ → Create a note
-   GET /api/notes/`<id>`{=html} → Get single note
-   PUT /api/notes/`<id>`{=html} → Update note
-   DELETE /api/notes/`<id>`{=html} → Delete note

------------------------------------------------------------------------

## Testing

Run tests using:

pytest

For coverage:

pytest --cov=website

------------------------------------------------------------------------

## Project Structure

website/ │ 
         ├── api/notes.py 
         ├── auth.py 
         ├── views.py 
         ├── models.py 
         ├──__init__.py 
         └── templates/

tests/ └── test_api.py

------------------------------------------------------------------------

## Notes

-   Swagger UI is available at /docs
-   API uses SQLite database
-   user_id is assigned using current_user when authenticated
