# Clash of Codes Server

This repository contains the backend server code for the **Clash of Codes** hackathon. The server is built using Django and provides necessary APIs and services for the hackathon participants.

- **Hackathon Name:** Clash of Codes
- **Server Repository:** [Clash of Codes Server](https://github.com/9147/ClashOfCodesServer)
- **Static Site Repository:** [Clash of Codes Static Site](https://github.com/9147/ClashOfCodes)

## Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## About the Project

The **Clash of Codes** hackathon server handles user registration, authentication, and API management for the hackathon. This backend is hosted on PythonAnywhere, while the frontend static site is hosted on GitHub Pages.

- **Static Site URL:** [Clash of Codes Static Site](https://github.com/9147/ClashOfCodes)
  
## Features

- User Registration and Authentication
- API for managing teams and participants
- Admin panel for managing events and users
- Secure Token-based authentication for participants
- Rate-limiting and email verification
- Integrated with the static site

## Tech Stack

- **Backend:** Django, Django REST Framework
- **Database:** SQLite (or any other configured DB in production)
- **Email:** Configured for email verification
- **Hosting:** PythonAnywhere

## Installation

To get a local copy up and running, follow these simple steps.

### Prerequisites

- Python 3.8+
- Virtual Environment (recommended)
- Django 3.2+
- Django REST Framework

### Installation Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/9147/ClashOfCodesServer.git
    ```

2. Navigate to the project directory:
    ```bash
    cd ClashOfCodesServer
    ```

3. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Create `.env` file and set the required environment variables (such as secret key, email config, etc.).

6. Apply migrations:
    ```bash
    python manage.py migrate
    ```

7. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

8. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Running the Server

To run the server locally:

```bash
python manage.py runserver
