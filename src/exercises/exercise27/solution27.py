import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import Counter


def create_sample_data():
    """
    Generate synthetic job execution data for testing.
    Returns DataFrame with columns: job_name, start_date_time, end_date_time,
    ingest_location, status
    """
    jobs = ['JobA', 'JobB', 'JobC', 'JobD', 'JobE']
    data = []

    start_date = datetime(2024, 1, 1)
    for job in jobs:
        current_date = start_date
        # Random frequency between 15 minutes and 1 week (in minutes)
        frequency = np.random.choice([15, 30, 60, 240, 1440, 10080])

        for _ in range(100):
            # Calculate normal duration as 50% of frequency with 10% standard deviation
            duration = np.random.normal(frequency * 0.5, frequency * 0.1)
            end_date = current_date + timedelta(minutes=duration)

            # 5% chance of extended runtime (3x normal duration)
            if np.random.random() < 0.05:
                duration *= 3
                end_date = current_date + timedelta(minutes=duration)

            data.append({
                'job_name': job,
                'start_date_time': current_date,
                'end_date_time': end_date,
                'ingest_location': f'/data/{job.lower()}',
                'status': np.random.choice(['Success', 'Failed'], p=[0.95, 0.05])
            })

            # Schedule next run after completion + frequency interval
            increment = max(timedelta(minutes=int(frequency)),
                            end_date - current_date + timedelta(minutes=int(frequency)))
            current_date += increment

    return pd.DataFrame(data)


def detect_job_frequency(time_diffs):
    """
    Analyze time differences between job runs to determine execution frequency.

    Args:
        time_diffs: pandas Series of timedelta objects between consecutive runs

    Returns:
        str: Human-readable description of detected frequency
    """
    # Convert time differences to minutes
    minutes_diff = time_diffs.dt.total_seconds() / 60

    # Remove outliers using IQR method
    q1, q3 = minutes_diff.quantile([0.25, 0.75])
    iqr = q3 - q1
    valid_diffs = minutes_diff[(minutes_diff >= q1 - 1.5 * iqr) &
                               (minutes_diff <= q3 + 1.5 * iqr)]

    # Get median interval after removing outliers
    median_interval = valid_diffs.median()

    # Standard scheduling intervals and their descriptions
    intervals = {
        15: "Every 15 minutes",
        30: "Every 30 minutes",
        60: "Hourly",
        120: "Every 2 hours",
        240: "Every 4 hours",
        360: "Every 6 hours",
        720: "Every 12 hours",
        1440: "Daily",
        10080: "Weekly",
        20160: "Bi-weekly"
    }

    # Find closest standard interval
    closest_interval = min(intervals.keys(),
                           key=lambda x: abs(x - median_interval))

    # Return custom interval if no standard interval matches within 20% tolerance
    if abs(closest_interval - median_interval) > closest_interval * 0.2:
        return f"Every {round(median_interval)} minutes"

    return intervals[closest_interval]


def analyze_job_schedules(df, output_file='job_analysis.csv'):
    """
    Analyze job execution patterns and performance metrics, export to CSV.

    Args:
        df: DataFrame with columns: job_name, start_date_time, end_date_time, status
        output_file: Name of the CSV file to export results

    Returns:
        DataFrame with analysis results per job and exports to CSV
    """
    # Convert timestamp columns and calculate execution duration
    df['start_date_time'] = pd.to_datetime(df['start_date_time'])
    df['end_date_time'] = pd.to_datetime(df['end_date_time'])
    df['execution_time'] = (df['end_date_time'] - df['start_date_time']).dt.total_seconds() / 60

    results = {}

    for job_name in df['job_name'].unique():
        # Analyze each job separately
        job_data = df[df['job_name'] == job_name].sort_values('start_date_time')

        # Calculate intervals between consecutive starts
        time_diffs = job_data['start_date_time'].diff()

        # Detect schedule pattern (skip first row with NaN diff)
        schedule = detect_job_frequency(time_diffs[1:])

        # Get earliest and latest run timestamps
        earliest_run = job_data['start_date_time'].min()
        latest_run = job_data['start_date_time'].max()

        # Compile metrics
        results[job_name] = {
            'job_name': job_name,
            'schedule': schedule,
            'avg_execution_time': job_data['execution_time'].mean(),
            'min_execution_time': job_data['execution_time'].min(),
            'max_execution_time': job_data['execution_time'].max(),
            'success_rate': (job_data['status'] == 'Success').mean() * 100,
            'total_runs': len(job_data),
            'median_interval_minutes': time_diffs[1:].dt.total_seconds().median() / 60,
            'earliest_run': earliest_run,
            'latest_run': latest_run
        }

    # Convert results to DataFrame
    results_df = pd.DataFrame(results).T

    # Reorder columns to match requested header
    column_order = [
        'job_name', 'schedule', 'avg_execution_time', 'min_execution_time',
        'max_execution_time', 'success_rate', 'total_runs',
        'median_interval_minutes', 'earliest_run', 'latest_run'
    ]
    results_df = results_df[column_order]

    # Export to CSV
    results_df.to_csv(output_file, index=False)
    print(f"Analysis results exported to {output_file}")

    return results_df


# Example usage
if __name__ == "__main__":
    # Generate and analyze sample data
    df = create_sample_data()
    results = analyze_job_schedules(df, 'job_analysis.csv')
    print("\nJob Analysis Results:")
    print(results.round(2))