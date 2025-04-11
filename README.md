# CarePlanner 🏥

A Python-based project with PostgreSQL backend for care planning management.

## Table of Contents
- [Prerequisites](#-prerequisites)
- [Setup Instructions](#%EF%B8%8F-setup-instructions)
  - [1. Install PostgreSQL](#1-install-postgresql-and-create-database)
  - [2. Clone Repository](#2-clone-repository)
  - [3. Virtual Environment](#3-create-and-activate-virtual-environment)
  - [4. Install Dependencies](#4-install-dependencies)
  - [5. Run Application](#5-run-the-application)
- [Default Credentials](#-default-credentials)

## 🚀 Prerequisites

Before you begin, ensure you have installed:
- [PostgreSQL](https://www.postgresql.org/download/)
- [Python 3.8+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [virtualenv](https://virtualenv.pypa.io/en/stable/)

## 🛠️ Setup Instructions

### 1. Install PostgreSQL and Create Database

1. Install PostgreSQL
2. Create the database:
```
psql -U postgres
CREATE DATABASE careplanner;
\q

```

### 2. Clone repository

```
git clone https://github.com/MuhamadAlee/carePlanner.git
cd carePlanner
```

### 3. Create and Activate Virtual Environment

```
python3 -m venv venv
source venv/bin/activate 
```

### 4. Install Dependencies
```
pip install -r requirements.txt
```

### 5. Run the Application
```
python source/api.py
```