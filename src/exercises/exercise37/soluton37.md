See below Python implementations for both jobs that handle the producer-consumer pattern with file-based
communication.I've created two Python scripts for your producer-consumer job pattern. Here's what each script does:

## Job 1 (Producer) - `job1_producer.py`

**Key Features:**

- Creates a JSON file with the format `data-mmddyyyy.json` (e.g., `data-08142025.json`)
- Uses atomic file operations (write to temp file, then rename) to prevent race conditions
- Includes comprehensive logging to both file and console
- Generates sample data with timestamps and metadata
- Creates a shared data directory if it doesn't exist

## Job 2 (Consumer) - `job2_consumer.py`

**Key Features:**

- Waits up to 2 hours for the expected JSON file to appear
- Checks every 30 seconds (configurable) for the file
- Verifies the file is readable and not empty before processing
- Includes detailed logging with remaining time information
- Processes the JSON data and creates a summary
- Saves processing results to a new file
- Raises `FileWaitTimeoutError` if timeout is exceeded

## Key Implementation Details:

1. **File Safety**: The producer uses atomic operations (write to `.tmp` file, then rename) to ensure the consumer never
   sees a partially written file.

2. **Robust Waiting**: The consumer checks file existence, size, and readability before proceeding.

3. **Configurable Parameters**:
    - Timeout period (default: 2 hours)
    - Check interval (default: 30 seconds)
    - Shared directory path (default: `./shared_data`)

4. **Error Handling**: Both scripts include comprehensive error handling and logging.

5. **Date-based Filenames**: Both scripts generate the same filename format based on the current date.

## Usage:

```bash
# Run the producer job
python job1_producer.py

# Run the consumer job (15-20 minutes later)
python job2_consumer.py
```

The scripts will create log files (`job1_producer.log` and `job2_consumer.log`) and share data through
the `./shared_data` directory. The consumer will process the data and create a `processed_data-mmddyyyy.json` file with
the results.