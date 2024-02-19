# [REPLACE ME]

## Installation Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Django Secret Key

```python
from django.core.management.utils import get_random_secret_key

# Generate a new secret key
new_secret_key = get_random_secret_key()

print(new_secret_key)
```
```
NOTE: Copy generated secret key
```

### 3. Create .env file in root directory

```bash
# Environment name (development or production)
ENVIRONMENT=name

# Generated secret key
SECRET_KEY=secret_key

# PRODUCTION ONLY

# Allowed hosts separated by ',' (eg. 127.0.0.1,localhost)
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 4. Create and apply migrations

```python
# Move into src directory
cd src/

# Apply migrations
python manage.py makemigrations
python manage.py migrate
```

### 5. Run Django server
```
python manage.py runserver
```