# ECO-CYCLE
A Flask-based backend API for a waste management system.

## Table of Contents

-   [Installation](#installation)
-   [Setup Guide](#setup-guide)
    -   [1. Flask + Flask-RESTful](#1-flask--flask-restful)
    -   [2. Flask-SQLAlchemy + Serializer](#2-flask-sqlalchemy--serializer)
    -   [3. Flask-Bcrypt + Flask-JWT-Extended](#3-flask-bcrypt--flask-jwt-extended)
-   [Running the Application](#running-the-application)
-   [API Endpoints](#api-endpoints)

## Installation

1. Clone the repository and navigate to the backend directory:

```bash
cd backend
```

2. Install dependencies using Pipenv:

```bash
pipenv install
```

3. Activate the virtual environment:

```bash
pipenv shell
```

4. Create a `.env` file in the backend directory (make sure to include it in the .gitignore file):

```bash
touch .env
```


## Setup Guide

### 1. Flask + Flask-RESTful

#### Installation

```bash
pipenv install flask flask-restful
```

#### Configuration (app.py)


<!-- Relationships -->
# Industry → Waste
One-to-Many (1:N)
One industry generates multiple waste streams over time.

# Industry → Request
One-to-Many (1:N)
One industry can issue multiple requests for waste collection or resource acquisition.

# Waste → Request
Many-to-Many (M:N)
Multiple requests might target the same type of waste, and one request might involve multiple waste types.

<!--
Ref: industry.id < waste.industry_id
Ref: industry.id < waste_requests.industry_id
Ref: waste.id < waste_requests.waste_id

 -->