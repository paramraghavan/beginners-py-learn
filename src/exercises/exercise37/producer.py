#!/usr/bin/env python3
"""
Job 1 - Producer Job
Creates a JSON file with current date in filename format: data-mmddyyyy.json
"""

import json
import os
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('job1_producer.log'),
        logging.StreamHandler()
    ]
)


def create_sample_data():
    """Create sample data for the JSON file"""
    return {
        "timestamp": datetime.now().isoformat(),
        "job_id": "job1_producer",
        "data": {
            "records": [
                {"id": 1, "name": "Sample Record 1", "value": 100},
                {"id": 2, "name": "Sample Record 2", "value": 200},
                {"id": 3, "name": "Sample Record 3", "value": 300}
            ],
            "metadata": {
                "total_records": 3,
                "created_by": "job1_producer",
                "version": "1.0"
            }
        }
    }


def generate_filename():
    """Generate filename in format: data-mmddyyyy.json"""
    now = datetime.now()
    return f"data-{now.strftime('%m%d%Y')}.json"


def produce_json_file(output_dir="./shared_data"):
    """Main function to produce the JSON file"""
    try:
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Generate filename and full path
        filename = generate_filename()
        filepath = os.path.join(output_dir, filename)

        logging.info(f"Starting Job 1 - Producer")
        logging.info(f"Creating file: {filepath}")

        # Create sample data
        data = create_sample_data()

        # Write to temporary file first, then rename (atomic operation)
        temp_filepath = f"{filepath}.tmp"

        with open(temp_filepath, 'w') as f:
            json.dump(data, f, indent=2)

        # Rename temp file to final filename (atomic operation)
        os.rename(temp_filepath, filepath)

        logging.info(f"Successfully created file: {filepath}")
        logging.info(f"File size: {os.path.getsize(filepath)} bytes")

        return filepath

    except Exception as e:
        logging.error(f"Error in Job 1 - Producer: {str(e)}")
        raise


if __name__ == "__main__":
    try:
        filepath = produce_json_file()
        print(f"Job 1 completed successfully. File created: {filepath}")
    except Exception as e:
        print(f"Job 1 failed: {str(e)}")
        exit(1)
