import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import Counter


def generate_sample_data(num_records=1000):
    np.random.seed(42)
    jobs = [f"Job_{chr(65 + i)}" for i in range(5)]  # Job_A through Job_E

    data = []
    current_time = datetime(2024, 1, 1)

    for _ in range(num_records):
        job_name = np.random.choice(jobs)

        # Different intervals for different jobs
        if job_name == "Job_A":
            interval = timedelta(minutes=30)
            duration = np.random.normal(25 * 60, 5 * 60)  # around 25 minutes
        elif job_name == "Job_B":
            interval = timedelta(hours=1)
            duration = np.random.normal(45 * 60, 10 * 60)  # around 45 minutes
        elif job_name == "Job_C":
            interval = timedelta(hours=24)
            duration = np.random.normal(120 * 60, 30 * 60)  # around 2 hours
        else:
            interval = timedelta(minutes=int(np.random.choice([15, 30, 60, 1440])))
            duration = np.random.normal(30 * 60, 10 * 60)  # around 30 minutes

        # Occasionally generate longer runs
        if np.random.random() < 0.05:
            duration *= 3

        start_time = current_time + timedelta(minutes=int(np.random.randint(-30, 30)))
        end_time = start_time + timedelta(seconds=int(abs(duration)))

        # Generate status with bias towards success
        status = np.random.choice(['Success', 'Failed', 'Running', 'Start'],
                                  p=[0.85, 0.10, 0.03, 0.02])

        data.append({
            'job_name': job_name,
            'start_date_time': start_time,
            'end_date_time': end_time,
            's3_location': f's3://bucket/{job_name}/{start_time.strftime("%Y/%m/%d/%H")}/',
            'status': status
        })

        current_time += interval

    return pd.DataFrame(data)


def detect_schedule_pattern(timestamps, intervals):
    """
    Sophisticated schedule detection that looks for various patterns in job execution times
    """
    # Convert timestamps to various components for pattern detection
    times = pd.DataFrame({
        'timestamp': timestamps,
        'hour': timestamps.dt.hour,
        'minute': timestamps.dt.minute,
        'day': timestamps.dt.day,
        'weekday': timestamps.dt.weekday,
        'month': timestamps.dt.month
    })

    # Get median interval in minutes
    median_interval = intervals.median()

    # Analyze hour patterns
    hour_counts = Counter(times['hour'])
    distinct_hours = sorted(hour_counts.keys())

    # Analyze minute patterns
    minute_counts = Counter(times['minute'])
    distinct_minutes = sorted(minute_counts.keys())

    # Analyze weekday patterns
    weekday_counts = Counter(times['weekday'])

    # Pattern detection logic
    if median_interval <= 15:
        # Check if it's exactly every 15 minutes
        if all(m % 15 == 0 for m in distinct_minutes):
            return "Every 15 minutes"
        return f"Approximately every {round(median_interval)} minutes"

    elif median_interval <= 30:
        if all(m % 30 == 0 for m in distinct_minutes):
            return "Every 30 minutes"
        return f"Approximately every {round(median_interval)} minutes"

    elif median_interval <= 60:
        if all(m == 0 for m in distinct_minutes):
            return "Hourly on the hour"
        return "Hourly"

    elif median_interval <= 180:
        hours = round(median_interval / 60)
        return f"Every {hours} hours"

    elif median_interval <= 1440:
        # Daily pattern detection
        if len(distinct_hours) == 1:
            hour = distinct_hours[0]
            return f"Daily at {hour:02d}:00"
        elif len(distinct_hours) > 1:
            hours_str = ", ".join(f"{h:02d}:00" for h in distinct_hours)
            return f"Daily at {hours_str}"

    elif median_interval <= 10080:  # Weekly
        if len(weekday_counts) == 1:
            weekday = list(weekday_counts.keys())[0]
            weekday_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][weekday]
            if len(distinct_hours) == 1:
                hour = distinct_hours[0]
                return f"Weekly on {weekday_name} at {hour:02d}:00"
            return f"Weekly on {weekday_name}"

    elif median_interval <= 43200:  # Monthly
        if len(set(times['day'])) == 1:
            day = times['day'].iloc[0]
            if len(distinct_hours) == 1:
                hour = distinct_hours[0]
                return f"Monthly on day {day} at {hour:02d}:00"
            return f"Monthly on day {day}"

    # If no specific pattern is detected
    if median_interval > 43200:
        return "Custom (> Monthly)"
    else:
        return f"Custom (~ every {round(median_interval)} minutes)"


def analyze_job_schedules(df):
    # Convert datetime columns to datetime type if they aren't already
    df['start_date_time'] = pd.to_datetime(df['start_date_time'])
    df['end_date_time'] = pd.to_datetime(df['end_date_time'])

    # Calculate execution time in seconds
    df['execution_time'] = (df['end_date_time'] - df['start_date_time']).dt.total_seconds()

    results = []

    for job_name in df['job_name'].unique():
        job_data = df[df['job_name'] == job_name].sort_values('start_date_time')

        # Calculate intervals between consecutive runs
        # intervals = (job_data['start_date_time'].diff().dt.total_seconds() / 60).dropna()
        intervals = (job_data['start_date_time'].diff().dt.total_seconds()).dropna()

        # Calculate success rate
        total_runs = len(job_data)
        success_runs = len(job_data[job_data['status'] == 'Success'])
        success_rate = (success_runs / total_runs) * 100 if total_runs > 0 else 0

        # Detect schedule pattern
        schedule = detect_schedule_pattern(job_data['start_date_time'], intervals)

        # Additional statistics
        std_interval = intervals.std()
        # schedule_consistency = (1 - (std_interval / intervals.mean())) * 100 if intervals.mean() > 0 else 0

        results.append({
            'job_name': job_name,
            'schedule': schedule,
            'avg_execution_time': round(job_data['execution_time'].mean(), 2),
            'min_execution_time': round(job_data['execution_time'].min(), 2),
            'max_execution_time': round(job_data['execution_time'].max(), 2),
            'success_rate': round(success_rate, 2),
            'total_runs': total_runs,
            'median_interval': round(intervals.median(), 2),
            'std_deviation_interval': round(std_interval, 2),
            'earliest_run': job_data['start_date_time'].min(),
            'latest_run': job_data['start_date_time'].max()
        })

    return pd.DataFrame(results)

# Example usage
if __name__ == "__main__":
    # Generate and analyze sample data
    df = generate_sample_data()

    # Save raw data to CSV
    df.to_csv('job_execution_data.csv', index=False)

    # Analyze the data
    results_df = analyze_job_schedules(df)

    # Format datetime columns and round numeric columns
    results_df['earliest_run'] = results_df['earliest_run'].dt.strftime('%Y-%m-%d %H:%M:%S')
    results_df['latest_run'] = results_df['latest_run'].dt.strftime('%Y-%m-%d %H:%M:%S')
    results_df = results_df.round({
        'avg_execution_time': 2,
        'min_execution_time': 2,
        'max_execution_time': 2,
        'success_rate': 2,
        'median_interval_minutes': 2
    })

    # Save results to CSV
    results_df.to_csv('job_schedule_analysis.csv', index=False)