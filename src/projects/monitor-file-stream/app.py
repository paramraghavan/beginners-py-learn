from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flashing messages

# Assuming file_monitor is your FileMonitor instance
file_monitor = None


@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Get current state
    df = file_monitor.state_tracker.get_dataframe()

    # Sort by latest in_time
    df = df.sort_values('in_time', ascending=False)

    # Calculate pagination
    total_records = len(df)
    total_pages = (total_records + per_page - 1) // per_page

    # Get subset for current page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    current_data = df.iloc[start_idx:end_idx]

    # Convert to list of dicts for template
    records = current_data.to_dict('records')

    return render_template(
        'file_monitor.html',
        records=records,
        page=page,
        total_pages=total_pages,
        total_records=total_records
    )


@app.route('/clear', methods=['POST'])
def clear_data():
    try:
        # Clear the DataFrame in thread-safe manner
        file_monitor.state_tracker.clear_data()
        # Store flash message in session
        flash('Data cleared successfully!', 'success')
    except Exception as e:
        # Store error message in session
        flash(f'Error clearing data: {str(e)}', 'error')
    return redirect(url_for('index'))


def start_web_interface(monitor_instance, host='0.0.0.0', port=5000):
    global file_monitor
    file_monitor = monitor_instance
    app.run(host=host, port=port)