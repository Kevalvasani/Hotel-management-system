from datetime import datetime, timedelta
import portion as P

def calculate_time_difference_excluding_nights(start_time, end_time):
    if start_time > end_time:
        raise ValueError("start_time must be before end_time")
    
    total_time = P.empty()
    current_time = start_time

    while current_time < end_time:
        # Determine the start and end of the valid interval for the current day
        day_start = current_time.replace(hour=6, minute=0, second=0, microsecond=0)
        day_end = current_time.replace(hour=23, minute=59, second=59, microsecond=999999)

        if current_time < day_start:
            current_time = day_start
        
        interval_start = max(current_time, day_start)
        interval_end = min(end_time, day_end)
        
        if interval_start < interval_end:
            total_time |= P.closedopen(interval_start, interval_end)

        # Move to the next day
        current_time = day_start + timedelta(days=1)

    # Calculate the total duration in seconds
    total_seconds = 0
    for interval in total_time:
        total_seconds += (interval.upper - interval.lower).total_seconds()

    # Convert total seconds to hours
    total_hours = total_seconds / 3600
    return total_hours

# Example usage
start_time = datetime(2024, 5, 18, 23, 0)  # Example start time
end_time = datetime(2024, 5, 20, 7, 0)    # Example end time

hours = calculate_time_difference_excluding_nights(start_time, end_time)
print(f"Total hours excluding nights: {hours:.2f}")
