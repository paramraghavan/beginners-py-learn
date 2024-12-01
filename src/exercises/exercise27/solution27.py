import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_sample_data(output_file='job_executions.csv', num_jobs=10, days=30):
    """Generate sample job execution data"""
    jobs = []

    # Define different job patterns
    patterns = [
        {'name': 'JobA', 'frequency': 30, 'unit': 'minutes', 'occasional_delay': True},
        {'name': 'JobB', 'frequency': 60, 'unit': 'minutes'},
        {'name': 'JobC', 'frequency': 24, 'unit': 'hours'},
        {'name': 'JobD', 'frequency': 1, 'unit': 'week'},
        {'name': 'JobE', 'times_per_day': [9, 15]},  # Runs at 9AM and 3PM
        {'name': 'JobF', 'frequency': 15, 'unit': 'minutes'},
        {'name': 'JobG', 'frequency': 12, 'unit': 'hours'},
        {'name': 'JobH', 'times_per_day': [8, 12, 16, 20]},  # Runs 4 times a day
        {'name': 'JobI', 'frequency': 2, 'unit': 'week'},
        {'name': 'JobJ', 'frequency': 1, 'unit': 'month'}
    ]

    start_date = datetime.now() - timedelta(days=days)

    for pattern in patterns:
        current_time = start_date
        job_name = pattern['name']

        while current_time < datetime.now():
            # Normal execution time between 5 and 15 minutes
            execution_time = random.randint(5, 15)

            # For JobA, occasionally have longer execution times
            if pattern.get('occasional_delay') and random.random() < 0.1:
                execution_time = random.randint(120, 180)  # 2-3 hours

            start_time = current_time
            end_time = start_time + timedelta(minutes=execution_time)

            # Determine status (90% success rate)
            status = random.choices(['Success', 'Failed'], weights=[90, 10])[0]

            jobs.append({
                'job_name': job_name,
                'start_date_time': start_time,
                'end_date_time': end_time,
                's3_location': f's3://job-logs/{job_name}/{start_time.strftime("%Y/%m/%d")}/',
                'status': status
            })

            # Calculate next run time based on pattern
            if 'frequency' in pattern:
                if pattern['unit'] == 'minutes':
                    increment = timedelta(minutes=pattern['frequency'])
                elif pattern['unit'] == 'hours':
                    increment = timedelta(hours=pattern['frequency'])
                elif pattern['unit'] == 'week':
                    increment = timedelta(weeks=pattern['frequency'])
                elif pattern['unit'] == 'month':
                    increment = timedelta(days=30 * pattern['frequency'])

                # For jobs with occasional delays, ensure next run is after completion
                if pattern.get('occasional_delay'):
                    current_time = max(end_time + timedelta(minutes=30),
                                       current_time + increment)
                else:
                    current_time += increment

            elif 'times_per_day' in pattern:
                # Move to next scheduled time
                current_date = current_time.date()
                next_time = None
                for hour in pattern['times_per_day']:
                    scheduled_time = datetime.combine(current_date,
                                                      datetime.min.time().replace(hour=hour))
                    if scheduled_time > current_time:
                        next_time = scheduled_time
                        break

                if next_time is None:  # Move to next day's first scheduled time
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
    """Analyze job execution patterns and generate schedule summary"""
    results = []

    for job_name in df['job_name'].unique():
        job_df = df[df['job_name'] == job_name].copy()

        # Calculate execution times in minutes
        job_df['execution_time'] = (job_df['end_date_time'] -
                                    job_df['start_date_time']).dt.total_seconds() / 60

        # Calculate intervals between starts
        job_df['interval'] = job_df['start_date_time'].diff().dt.total_seconds() / 60

        # Basic statistics
        avg_exec_time = job_df['execution_time'].mean()
        std_dev_exec_time = job_df['execution_time'].std()
        min_exec_time = job_df['execution_time'].min()
        max_exec_time = job_df['execution_time'].max()
        success_rate = (job_df['status'] == 'Success').mean() * 100
        total_runs = len(job_df)
        median_interval = job_df['interval'].median()
        earliest_run = job_df['start_date_time'].min()
        latest_run = job_df['start_date_time'].max()

        # Determine schedule pattern
        schedule = "Unknown"

        # Check if job runs at specific times
        job_df['hour'] = job_df['start_date_time'].dt.hour
        unique_hours = sorted(job_df['hour'].unique())
        if len(unique_hours) <= 4:  # If job runs at specific hours
            times = [f"{hour:02d}:00" for hour in unique_hours]
            schedule = f"Daily at {', '.join(times)}"
        else:
            # Check for regular intervals
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

        results.append({
            'job_name': job_name,
            'schedule': schedule,
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

# Save results
results_df.to_csv('job_schedule_analysis.csv', index=False)

# Display results
print("\nJob Schedule Analysis:")
print(results_df.to_string())