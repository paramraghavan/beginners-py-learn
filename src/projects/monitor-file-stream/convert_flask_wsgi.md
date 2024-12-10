# How to convert a Flask app to work with a WSGI server. 

1. First, here's how a typical Flask app looks:

```python
# app.py
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
```

2. To make it WSGI compatible, you just need to expose the Flask app instance:

```python
# app.py
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello World!'


# This is the WSGI entry point
application = app

if __name__ == '__main__':
    app.run()
```

3. To run with Gunicorn (a popular WSGI server):

```bash
# Install gunicorn
pip install gunicorn

# Run the app
gunicorn app:application
```

4. If you want to use uWSGI:

```bash
# Install uwsgi
pip install uwsgi

# Run the app
uwsgi --http :8000 --wsgi-file app.py --callable application
```

5. For more complex configurations, you can create a WSGI configuration file:

```python
# wsgi.py
from app import app

if __name__ == "__main__":
    app.run()
```

6. Example configuration for production deployment with Gunicorn:

```bash
gunicorn --workers 4 --bind 0.0.0.0:8000 wsgi:app
```

Key points:

- The Flask app instance itself is already WSGI-compatible
- You just need to expose it as a WSGI application
- The main changes are in how you deploy it, not in the application code
- The development server (`app.run()`) should only be used for development

Common configuration options for production:

```python
# config.py
bind = "0.0.0.0:8000"
workers = 4
timeout = 120
accesslog = "access.log"
errorlog = "error.log"
```

Save this as `gunicorn.conf.py` and run:

```bash
gunicorn -c gunicorn.conf.py app:app
```

Remember:

- Always use a WSGI server in production
- Never use Flask's built-in server in production
- Consider using environment variables for configuration
- Set appropriate number of workers based on your CPU cores (typically 2-4 x number of CPU cores)