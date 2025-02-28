# My Django Project

This is a Django project that includes RESTful APIs for user signup and signin, as well as CRUD operations for the Pin model. The project is integrated with a Google Cloud Platform (GCP) PostgreSQL database and includes functionality to migrate and seed the database with initial data.

## Project Structure

```
pin_tracker_app
├── pin_tracker_app
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── pins
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── fixtures
│   │   └── initial_data.json
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── users
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd pin_tracker_app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```
   pip install -r requirements.txt
   ```

4. **Configure the database:**
   Update the `DATABASES` setting in `pin_tracker_app/settings.py` to connect to your GCP PostgreSQL database.

5. **Run migrations:**
   ```
   python manage.py migrate
   ```

6. **Load initial data:**
   ```
   python manage.py loaddata pins/fixtures/initial_data.json
   ```

7. **Run the development server:**
   ```
   python manage.py runserver
   ```

## Usage

- **User Signup:** POST request to `/users/signup/` with email and password.
- **User Signin:** POST request to `/users/signin/` with email and password.
- **CRUD Operations for Pins:**
  - Create: POST request to `/pins/`
  - Read: GET request to `/pins/` or `/pins/<id>/`
  - Update: PUT/PATCH request to `/pins/<id>/`
  - Delete: DELETE request to `/pins/<id>/`

## License

This project is licensed under the MIT License.