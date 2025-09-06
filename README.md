# Food Order App - Local Setup Guide

This guide provides instructions to set up and run the Food Order App on your local machine. Follow these steps carefully to get the application up and running.

## 1. Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.8+**: The application is developed using Python. You can download it from [python.org](https://www.python.org/downloads/).
- **pip**: Python's package installer. It usually comes with Python.
- **Git**: For cloning the repository. Download from [git-scm.com](https://git-scm.com/downloads).

## 2. Setup Instructions

### Step 2.1: Clone the Repository

First, clone the application repository to your local machine using Git:

```bash
git clone https://github.com/Mdboniamin/predefense.git
cd predefense
```

### Step 2.2: Create a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies. This prevents conflicts with other Python projects.

```bash
python3 -m venv venv
```

### Step 2.3: Activate the Virtual Environment

- **On Windows:**

  ```bash
  .\venv\Scripts\activate
  ```

- **On macOS/Linux:**

  ```bash
  source venv/bin/activate
  ```

### Step 2.4: Install Dependencies

Once the virtual environment is activated, install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### Step 2.5: Database Setup

The application uses SQLite as its database. You need to initialize the database and seed it with some dummy data.

```bash
python run.py db_init
python seed_data.py
```

### Step 2.6: Run the Application

After setting up the database, you can run the Flask application:

```bash
python run.py
```

This will start the development server, and the application will be accessible at `http://127.0.0.1:5000` in your web browser.

## 3. Demo Credentials

Use the following credentials to log in and test the application:

- **Admin:** admin@foodapp.com / admin123
- **Restaurant:** restaurant@foodapp.com / restaurant123  
- **Customer:** customer@foodapp.com / customer123

## 4. Troubleshooting

- **`ModuleNotFoundError`**: Ensure you have activated your virtual environment and installed all dependencies using `pip install -r requirements.txt`.
- **Database errors**: If you encounter issues with the database, try deleting `instance/site.db` (if it exists) and re-running `python run.py db_init` and `python seed_data.py`.
- **Port already in use**: If port 5000 is already in use, you might see an error. You can try running the app on a different port by modifying `run.py` or finding and terminating the process using port 5000.

---

**Author:** Manus AI
**Date:** 7/19/2025


