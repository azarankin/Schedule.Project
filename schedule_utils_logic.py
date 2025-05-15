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
    schedule, task_list = read_schedule_with_tasklist(CONFIG["SCHEDULE_FILE"])
    if not schedule:
        return None, [], task_list
    full_schedule = adjust_schedule_for_midnight(schedule, now)
    filtered = [(t, task) for t, task in full_schedule if -3 <= (t - now).total_seconds() / 3600 <= 5]
    if len(filtered) >= 9:
        return schedule, filtered, task_list
    i = min(range(len(full_schedule)), key=lambda i: abs((full_schedule[i][0] - now).total_seconds()))
    start, end = max(0, i - 3), min(len(full_schedule), i + 6)
    return schedule, full_schedule[start:end], task_list

def find_current_task_index(tasks_to_display, now):
    # search by diff +-30 min from current time
    for tolerance in [1800, 3600, 7200, 10800, 18000]:  # 30min, 1h, 2h, 3h, 4h, 5h
        closest = None
        min_diff = float('inf')
        for i, (task_time, _) in enumerate(tasks_to_display):
            delta = (task_time - now).total_seconds()
            if -tolerance <= delta <= tolerance and abs(delta) < min_diff:
                closest = i
                min_diff = abs(delta)
        if closest is not None:
            return closest

    # continue search for closest
    closest_past = None
    min_past_diff = float('inf')
    for i, (task_time, _) in enumerate(tasks_to_display):
        delta = (task_time - now).total_seconds()
        if delta < 0 and abs(delta) < min_past_diff:
            closest_past = i
            min_past_diff = abs(delta)

    # return the closest from both directions
    if closest_past is not None:
        return closest_past

    return min(range(len(tasks_to_display)), key=lambda i: abs((tasks_to_display[i][0] - now).total_seconds()))


def read_schedule_with_tasklist(file_path):
    schedule = []
    task_list = []
    inside_task_list = False

    if not os.path.exists(file_path):
        return schedule, task_list

    with open(file_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Begin Task List
            if line.lower().startswith("task_list"):
                inside_task_list = True
                continue

            # List line
            if inside_task_list:
                if line.startswith("-"):
                    task_list.append(  line.strip()  )
                continue
            
            # Comma seperated value
            if ',' in line:
                time_str, task = (line + ',').split(",", 1)[:2]
                time_str = time_str.strip().rstrip(',')
                task = task.strip().rstrip(',')
                if not time_str or not task.strip() or task.strip() ==',':
                    continue
                try:
                    
                    time = datetime.strptime(time_str, "%H:%M").time()
                    schedule.append((time, task))
                except ValueError:
                    #time_str == 'task,'
                    continue

    return schedule, task_list

