# schedule_logic.py
import csv
import os
from datetime import datetime, timedelta
from schedule_config import CONFIG

def read_schedule(file_path):
    if not os.path.exists(file_path):
        return []
    schedule = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        for row in csv.DictReader(csvfile):
            task = (row.get('task') or '').strip()
            time_str = (row.get('time') or '').strip()
            if not task or not time_str:
                continue
            try:
                time = datetime.strptime(time_str, "%H:%M").time()
                schedule.append((time, task))
            except ValueError:
                continue
    return schedule

def adjust_schedule_for_midnight(schedule, now):
    adjusted = []
    for t, task in schedule:
        task_dt = datetime.combine(now.date(), t)
        if t.hour < 3 and now.hour >= 21:
            task_dt += timedelta(days=1)
        elif t.hour >= 21 and now.hour < 3:
            task_dt -= timedelta(days=1)
        adjusted.append((task_dt, task))
    return adjusted

def load_and_filter_schedule(now):
    schedule = read_schedule(CONFIG["SCHEDULE_FILE"])
    if not schedule:
        return None, []
    full_schedule = adjust_schedule_for_midnight(schedule, now)
    filtered = [(t, task) for t, task in full_schedule if -3 <= (t - now).total_seconds() / 3600 <= 5]
    if len(filtered) >= 9:
        return schedule, filtered
    i = min(range(len(full_schedule)), key=lambda i: abs((full_schedule[i][0] - now).total_seconds()))
    start, end = max(0, i - 3), min(len(full_schedule), i + 6)
    return schedule, full_schedule[start:end]

def find_current_task_index(tasks_to_display, now):
    closest_now = None
    min_now_diff = float('inf')
    closest_past = None
    min_past_diff = float('inf')
    for i, (task_time, _) in enumerate(tasks_to_display):
        diff = abs((task_time - now).total_seconds())
        if (task_time >= now) and diff <= 1800 and diff < min_now_diff:
            closest_now = i
            min_now_diff = diff
        if task_time < now and diff < min_past_diff:
            closest_past = i
            min_past_diff = diff
    return closest_now if closest_now is not None else closest_past
