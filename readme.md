# Clash of Codes Hackathon Website

Welcome to the official repository for **Clash of Codes**, a hackathon inspired by the excitement and intensity of coding battles, similar to the **Clash of Clans** game. This site is designed to provide all the necessary information about our hackathon, which is set to take place on **November 29th and 30th**. The website is built using the **Django** framework and provides participants with essential event details, registration information, schedules, and more.

## Hackathon Overview

**Clash of Codes** is a competitive programming event where developers from all levels come together to solve real-world problems in a challenging, fun, and innovative environment. The event will feature various tracks and challenges designed to push your coding skills to the limit.

- **Date**: November 29th & 30th, 2024
- **Location**: KLS Gogte INstitute Of Engineering, Belagavi
- **Event URL**: [clashofcodes.in](https://clashofcodes.in)

## Features

- **Event Registration**: Allows users to register for the event.
- **Event Schedule**: Displays the detailed timeline of the hackathon.
- **Problem Statements**: Provides challenges for participants to solve during the hackathon.
- **Contact Information**: Provides ways to reach out to the organizing team.

## Technology Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (can be switched to PostgreSQL or MySQL for production)
- **Deployed on**: Hosted on [clashofcodes.in](https://clashofcodes.in)

## Installation & Setup

To get a local copy of the site up and running for development purposes, follow these steps:

### Prerequisites
- Python 3.10
- Django 5.1.1
- Git

### Steps

1. **Clone the repository**:
    `git clone https://github.com/9147/clashofcodes.git`
    `cd clashofcodes`

2. **Create a virtual environment and activate it**:
    `python3 -m venv env`
    `source env/bin/activate  `
    # On Windows use `env\\Scripts\\activate`
    

3. **Install the dependencies**:
    
    `pip install -r requirements.txt`
    

4. **Run migrations**:
    
    `python manage.py migrate`
    

5. **Run the development server**:
    
    `python manage.py runserver`
    

Visit `http://127.0.0.1:8000/` in your browser to view the site.




