# Dashboard Travel - Django Project

## Overview
Dashboard Travel is a Django-based project for managing travel operations, including passengers, drivers, vehicles, and trips. It provides an interface to manage these entities and supports media uploads for associated images.

---

## Features
- Passenger and driver management
- Vehicle and trip handling
- Image and file uploads
- Dashboard interface with analytics
- Structured templates and static files for design

---

## Prerequisites
Before setting up the project, ensure you have the following installed on your system:
- Python 3.9+
- XAMPP 8.2.12
- pip (Python package manager)
- Git
- Virtualenv (optional but recommended)

---

## Setup Instructions

### Step 1: Clone the Repository
Clone the project from the GitHub repository:
```bash
git clone https://github.com/yourusername/dashboard-travel.git
cd dashboard-travel
```

### Step 2: Create a Virtual Environment
Create and activate a virtual environment to isolate project dependencies:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
Install the required Python packages using `pip`:
```bash
pip install -r requirements.txt
```

### Step 4: Configure the Database
1. Open the `settings.py` file located in the `sanaanitravel` directory.
2. Update the `DATABASES` configuration to match your database credentials.
   Example for SQLite (default):
   ```python
      DATABASES = {
             'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'sanaanitravelproject',#اسم قاعدة البيانات
             'USER': 'root',# اسم المستخدم 
             'PASSWORD': '',#كلمة السر
             'HOST': 'localhost',
             'PORT': '3306',
         }
      }
   ```


```bash

      cd sanaanitravel

```
### Step 5: Apply Migrations
Run the following commands to create the necessary database tables:




```bash
python manage.py makemigrations
python manage.py migrate

```

```bash
python manage.py populate_data
```

### Step 6: Create a Superuser
Create an admin account to access the Django admin panel:
```bash
python manage.py createsuperuser
```
Follow the prompts to set up the superuser credentials.

### Step 7: Collect Static Files
Gather static files into a single location for production use:
```bash
python manage.py collectstatic
```

### Step 8: Run the Development Server
Start the Django development server:
```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000/`.

---

## Folder Structure
```
project-root/
├── dashboardtravel/
│   ├── control/         # Custom commands and logic
│   ├── management/      # Management commands
│   ├── migrations/      # Database migration files
│   ├── templates/       # HTML templates
│   └── __pycache__/     # Python cache files
├── media/               # Uploaded media files
│   ├── driver_images/
│   ├── passenger_images/
│   ├── trip_images/
│   └── vehicle_images/
├── sanaanitravel/       # Core project settings and configurations
│   ├── static/          # Static files (CSS, JS, Images)
│   ├── templates/       # Additional templates
│   └── __pycache__/     # Python cache files
└── static/              # Collected static files for production
```

---

## Deployment (Optional)

To deploy this project on a production server:

1. **Set Up Gunicorn and Nginx**:
   - Install Gunicorn: `pip install gunicorn`
   - Configure Gunicorn to serve the application.
   - Set up Nginx as a reverse proxy to Gunicorn.

2. **Set Debug to False**:
   In `settings.py`, set:
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   ```

3. **Configure a Production Database**:
   Update the `DATABASES` settings to use a production database like PostgreSQL.

4. **Serve Static and Media Files**:
   Use `collectstatic` to gather all static files and serve them via Nginx.



