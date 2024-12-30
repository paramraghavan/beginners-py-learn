from flask import Flask, render_template, request, send_file, jsonify
import pandas as pd
import io
import os

app = Flask(__name__)

# Global variable to store the DataFrame
global_df = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    global global_df
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Please upload a CSV file'}), 400

    try:
        # Read CSV file into DataFrame
        global_df = pd.read_csv(file)
        # Convert DataFrame to dict for JSON response
        data = {
            'columns': global_df.columns.tolist(),
            'data': global_df.values.tolist()
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/get_data')
def get_data():
    global global_df
    if global_df is None:
        return jsonify({'error': 'No data loaded'}), 400

    # Get pagination parameters
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))

    # Calculate start and end indices
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size

    # Slice the DataFrame
    page_df = global_df.iloc[start_idx:end_idx]

    data = {
        'columns': global_df.columns.tolist(),
        'data': page_df.values.tolist(),
        'total_rows': len(global_df),
        'total_pages': -(-len(global_df) // page_size)  # Ceiling division
    }
    return jsonify(data)


@app.route('/download')
def download():
    global global_df
    if global_df is None:
        return jsonify({'error': 'No data to download'}), 400

    # Create a buffer
    buffer = io.StringIO()
    global_df.to_csv(buffer, index=False)
    buffer.seek(0)

    return send_file(
        io.BytesIO(buffer.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='exported_data.csv'
    )


@app.route('/clear')
def clear():
    global global_df
    global_df = None
    return jsonify({'message': 'Data cleared successfully'})


if __name__ == '__main__':
    app.run(debug=True)
