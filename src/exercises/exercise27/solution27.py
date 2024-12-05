import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_sample_data(output_file='job_executions.csv', num_jobs=10, days=30):
    """
    Generate sample job execution data with various scheduling patterns.

    Args:
        output_file (str): Path to save the generated CSV file
        num_jobs (int): Number of different jobs to generate (not used currently as patterns are predefined)
        days (int): Number of days of historical data to generate

    Returns:
        pandas.DataFrame: Generated job execution data
    """
    jobs = []

    # Define different job patterns to simulate various real-world scenarios
    patterns = [
        {'name': 'JobA', 'frequency': 30, 'unit': 'minutes', 'occasional_delay': True},  # Job that sometimes runs long
        {'name': 'JobB', 'frequency': 60, 'unit': 'minutes'},  # Hourly job
        {'name': 'JobC', 'frequency': 24, 'unit': 'hours'},  # Daily job
        {'name': 'JobD', 'frequency': 1, 'unit': 'week'},  # Weekly job
        {'name': 'JobE', 'times_per_day': [9, 15]},  # Runs twice daily at fixed times
        {'name': 'JobF', 'frequency': 15, 'unit': 'minutes'},  # Runs every 15 minutes
        {'name': 'JobG', 'frequency': 12, 'unit': 'hours'},  # Runs twice daily
        {'name': 'JobH', 'times_per_day': [8, 12, 16, 20]},  # Runs 4 times daily
        {'name': 'JobI', 'frequency': 2, 'unit': 'week'},  # Bi-weekly job
        {'name': 'JobJ', 'frequency': 1, 'unit': 'month'}  # Monthly job
    ]

    # Calculate start date for data generation
    start_date = datetime.now() - timedelta(days=days)

    # Generate data for each job pattern
    for pattern in patterns:
        current_time = start_date
        job_name = pattern['name']

        while current_time < datetime.now():
            # Generate random execution time (5-15 minutes normally)
            execution_time = random.randint(5, 15)

            # Special handling for JobA - occasionally runs much longer (2-3 hours)
            if pattern.get('occasional_delay') and random.random() < 0.1:
                execution_time = random.randint(120, 180)

            # Calculate job start and end times
            start_time = current_time
            end_time = start_time + timedelta(minutes=execution_time)

            # Simulate job success/failure (90% success rate)
            status = random.choices(['Success', 'Failed'], weights=[90, 10])[0]

            # Create job execution record
            jobs.append({
                'job_name': job_name,
                'start_date_time': start_time,
                'end_date_time': end_time,
                's3_location': f's3://job-logs/{job_name}/{start_time.strftime("%Y/%m/%d")}/',
                'status': status
            })

            # Calculate next run time based on job pattern
            if 'frequency' in pattern:
                # Handle frequency-based schedules (every X minutes/hours/weeks/months)
                if pattern['unit'] == 'minutes':
                    increment = timedelta(minutes=pattern['frequency'])
                elif pattern['unit'] == 'hours':
                    increment = timedelta(hours=pattern['frequency'])
                elif pattern['unit'] == 'week':
                    increment = timedelta(weeks=pattern['frequency'])
                elif pattern['unit'] == 'month':
                    increment = timedelta(days=30 * pattern['frequency'])

                # For jobs with occasional delays (like JobA), ensure next run starts after completion
                if pattern.get('occasional_delay'):
                    current_time = max(end_time + timedelta(minutes=30),
                                       current_time + increment)
                else:
                    current_time += increment

            elif 'times_per_day' in pattern:
                # Handle fixed-time schedules (runs at specific times each day)
                current_date = current_time.date()
                next_time = None

                # Find next scheduled time for today
                for hour in pattern['times_per_day']:
                    scheduled_time = datetime.combine(current_date,
                                                      datetime.min.time().replace(hour=hour))
                    if scheduled_time > current_time:
                        next_time = scheduled_time
                        break

                # If no more runs today, move to first run of next day
                if next_time is None:
                    current_date += timedelta(days=1)
                    next_time = datetime.combine(current_date,
                                                 datetime.min.time().replace(
                                                     hour=pattern['times_per_day'][0]))

                current_time = next_time

    # Create DataFrame and save to CSV
    df = pd.DataFrame(jobs)
    df.sort_values('start_date_time', inplace=True)
    df.to_csv(output_file, index=False)
    return df


def analyze_job_schedules(df):
    """
    Analyze job execution patterns and generate schedule summary.

    Args:
        df (pandas.DataFrame): Input DataFrame containing job execution data

    Returns:
        pandas.DataFrame: Analysis results with schedule patterns and statistics
    """
    results = []
    """
        convert UTC to EST
        2024-11-25T14:33:09364354Z 
        Above  is a UTC timestamp in ISO 8601 format. The 'Z' at the end specifically indicates UTC

        Date: 2024-11-25
        Time: 14:33:09
        Microseconds: 364354
        Z: UTC timezone indicator
        df['est_time'] = pd.to_datetime(df['utc_column']).dt.tz_localize('UTC').dt.tz_convert('America/New_York')
    """
    # Convert datetime columns to datetime type if they aren't already
    df['start_date_time'] = pd.to_datetime(df['start_date_time'])
    df['end_date_time'] = pd.to_datetime(df['end_date_time'])

    # Analyze each job separately
    for job_name in df['job_name'].unique():
        job_df = df[df['job_name'] == job_name].copy()

        # Calculate execution times in minutes
        job_df['execution_time'] = (job_df['end_date_time'] -
                                    job_df['start_date_time']).dt.total_seconds() / 60

        # Calculate intervals between consecutive starts
        job_df['interval'] = job_df['start_date_time'].diff().dt.total_seconds() / 60

        # Add date column for daily run calculation
        job_df['date'] = job_df['start_date_time'].dt.date

        # Calculate runs per day statistics
        daily_runs = job_df.groupby('date').size()
        avg_runs_per_day = daily_runs.mean()
        min_runs_per_day = daily_runs.min()
        max_runs_per_day = daily_runs.max()

        # Calculate basic statistics
        avg_exec_time = job_df['execution_time'].mean()
        std_dev_exec_time = job_df['execution_time'].std()
        min_exec_time = job_df['execution_time'].min()
        max_exec_time = job_df['execution_time'].max()
        success_rate = (job_df['status'] == 'Success').mean() * 100
        total_runs = len(job_df)
        median_interval = job_df['interval'].median()
        earliest_run = job_df['start_date_time'].min()
        latest_run = job_df['start_date_time'].max()

        # Determine schedule pattern through analysis
        schedule = "Unknown"

        # Check if job runs at specific times of day
        job_df['hour'] = job_df['start_date_time'].dt.hour
        unique_hours = sorted(job_df['hour'].unique())

        # If job runs at 4 or fewer distinct hours, it's likely scheduled at fixed times
        if len(unique_hours) <= 4:
            times = [f"{hour:02d}:00" for hour in unique_hours]
            schedule = f"Daily at {', '.join(times)}"
        else:
            # Otherwise, determine the frequency based on median interval
            if median_interval < 60:  # Less than hourly
                schedule = f"Every {int(round(median_interval))} minutes"
            elif median_interval < 1440:  # Less than daily
                hours = round(median_interval / 60, 1)
                schedule = f"Every {hours} hours"
            elif median_interval < 10080:  # Less than weekly
                days = round(median_interval / 1440, 1)
                schedule = f"Every {days} days"
            else:  # Weekly or longer
                weeks = round(median_interval / 10080, 1)
                schedule = f"Every {weeks} weeks"

        # Format daily frequency description
        if avg_runs_per_day >= 1:
            daily_freq = (f"Runs {avg_runs_per_day:.1f} times per day on average "
                          f"(min: {min_runs_per_day}, max: {max_runs_per_day})")
        else:
            daily_freq = "Runs less than once per day"

        # Compile results for this job
        results.append({
            'job_name': job_name,
            'schedule': schedule,
            'daily_frequency': daily_freq,
            'avg_runs_per_day': round(avg_runs_per_day, 2),
            'min_runs_per_day': min_runs_per_day,
            'max_runs_per_day': max_runs_per_day,
            'avg_execution_time': round(avg_exec_time, 2),
            'std_dev_execution_time': round(std_dev_exec_time, 2),
            'min_execution_time': round(min_exec_time, 2),
            'max_execution_time': round(max_exec_time, 2),
            'success_rate': round(success_rate, 2),
            'total_runs': total_runs,
            'median_interval_minutes': round(median_interval, 2),
            'earliest_run': earliest_run,
            'latest_run': latest_run
        })

    return pd.DataFrame(results)


# Generate sample data
df = generate_sample_data()

# Analyze schedules
results_df = analyze_job_schedules(df)

# Save results to CSV
results_df.to_csv('job_schedule_analysis.csv', index=False)

# Display results
print("\nJob Schedule Analysis:")
print(results_df.to_string())