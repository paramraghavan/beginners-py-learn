#!/usr/bin/env python3
"""
Job 2 - Consumer Job
Waits for JSON file created by Job 1 and processes it.
Waits up to 2 hours before timing out.
"""

import json
import os
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('job2_consumer.log'),
        logging.StreamHandler()
    ]
)


class FileWaitTimeoutError(Exception):
    """Custom exception for file wait timeout"""
    pass


def generate_expected_filename():
    """Generate expected filename in format: data-mmddyyyy.json"""
    now = datetime.now()
    return f"data-{now.strftime('%m%d%Y')}.json"


def wait_for_file(filepath, timeout_hours=2, check_interval=30):
    """
    Wait for file to exist and be readable

    Args:
        filepath: Path to the file to wait for
        timeout_hours: Maximum hours to wait
        check_interval: Seconds between checks

    Raises:
        FileWaitTimeoutError: If timeout is reached
    """
    timeout_seconds = timeout_hours * 3600
    start_time = time.time()
    end_time = start_time + timeout_seconds

    logging.info(f"Waiting for file: {filepath}")
    logging.info(f"Timeout: {timeout_hours} hours")
    logging.info(f"Check interval: {check_interval} seconds")

    while time.time() < end_time:
        if os.path.exists(filepath):
            # Check if file is readable and not empty
            try:
                if os.path.getsize(filepath) > 0:
                    # Try to open and read a bit to ensure it's not being written
                    with open(filepath, 'r') as f:
                        f.read(1)  # Read first character to test readability
                    logging.info(f"File found and accessible: {filepath}")
                    return True
                else:
                    logging.info(f"File exists but is empty, continuing to wait...")
            except (IOError, OSError) as e:
                logging.info(f"File exists but not ready (may be being written): {e}")

        # Calculate remaining time
        remaining_seconds = end_time - time.time()
        remaining_minutes = remaining_seconds / 60

        if remaining_seconds > 0:
            logging.info(f"File not ready yet. Waiting... ({remaining_minutes:.1f} minutes remaining)")
            time.sleep(check_interval)
        else:
            break

    raise FileWaitTimeoutError(f"Timeout reached. File not found after {timeout_hours} hours: {filepath}")


def process_json_file(filepath):
    """Process the JSON file created by Job 1"""
    logging.info(f"Processing file: {filepath}")

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)

        # Process the data (example processing)
        logging.info("Processing data...")

        # Extract information
        timestamp = data.get('timestamp')
        job_id = data.get('job_id')
        records = data.get('data', {}).get('records', [])
        metadata = data.get('data', {}).get('metadata', {})

        logging.info(f"Original job ID: {job_id}")
        logging.info(f"File timestamp: {timestamp}")
        logging.info(f"Number of records: {len(records)}")
        logging.info(f"Total records (metadata): {metadata.get('total_records')}")

        # Example processing: calculate sum of values
        total_value = sum(record.get('value', 0) for record in records)
        logging.info(f"Total value from all records: {total_value}")

        # Create processed result
        processed_data = {
            "processed_timestamp": datetime.now().isoformat(),
            "processor_job_id": "job2_consumer",
            "source_file": filepath,
            "source_timestamp": timestamp,
            "processing_results": {
                "total_records_processed": len(records),
                "total_value": total_value,
                "average_value": total_value / len(records) if records else 0,
                "processing_status": "completed"
            }
        }

        # Save processed result
        output_filename = f"processed_{os.path.basename(filepath)}"
        output_path = os.path.join(os.path.dirname(filepath), output_filename)

        with open(output_path, 'w') as f:
            json.dump(processed_data, f, indent=2)

        logging.info(f"Processing completed. Result saved to: {output_path}")
        return processed_data

    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON file: {e}")
        raise
    except Exception as e:
        logging.error(f"Error processing file: {e}")
        raise


def consume_json_file(input_dir="./shared_data", timeout_hours=2):
    """Main function to consume the JSON file"""
    try:
        logging.info("Starting Job 2 - Consumer")

        # Generate expected filename
        filename = generate_expected_filename()
        filepath = os.path.join(input_dir, filename)

        # Wait for file to be available
        wait_for_file(filepath, timeout_hours)

        # Process the file
        result = process_json_file(filepath)

        logging.info("Job 2 - Consumer completed successfully")
        return result

    except FileWaitTimeoutError as e:
        logging.error(f"Timeout error: {e}")
        raise
    except Exception as e:
        logging.error(f"Error in Job 2 - Consumer: {str(e)}")
        raise


if __name__ == "__main__":
    try:
        result = consume_json_file()
        print("Job 2 completed successfully")
        print(f"Processing results: {result['processing_results']}")
    except FileWaitTimeoutError as e:
        print(f"Job 2 failed due to timeout: {str(e)}")
        exit(1)
    except Exception as e:
        print(f"Job 2 failed: {str(e)}")
        exit(1)
