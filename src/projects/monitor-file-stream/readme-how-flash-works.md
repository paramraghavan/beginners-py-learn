# Flash message, secret key and how it is used with Flask.

**The secret key is crucial because:**
1. It encrypts session data
2. Prevents tampering with flash messages
3. Ensures secure communication between server and client
4. Required for Flask's session management

**How flash works behind the scenes:**

```python
# 1. When flash() is called:
flash('Data cleared successfully!', 'success')
# - Message is stored in session
# - Session is encrypted using secret_key
# - Encrypted data sent to client as cookie

# 2. On next request:
# - Cookie is decrypted using secret_key
# - Messages retrieved from session
# - Messages displayed in template
# - Messages cleared from session
```

1. In the Flask Application:
```python
from flask import Flask, flash, render_template

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/clear', methods=['POST'])
def clear_data():
    try:
        # Clear the data
        file_monitor.state_tracker.clear_data()
        # Store flash message in session
        flash('Data cleared successfully!', 'success')
    except Exception as e:
        # Store error message in session
        flash(f'Error clearing data: {str(e)}', 'error')
        
    return redirect(url_for('index'))
```

2. In the HTML Template:
```html
<!-- Display flash messages -->
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="flash-message flash-{{ category }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
{% endwith %}
```


3. Example with multiple flash messages:

```python
@app.route('/process')
def process_files():
    try:
        # Start processing
        flash('Starting file processing...', 'info')
        
        if success:
            flash('Processing complete!', 'success')
        else:
            flash('Some files failed', 'warning')
            
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        
    return redirect(url_for('index'))
```
