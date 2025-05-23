from datetime import datetime, timedelta
from schedule_utils_ui_render import setup_hebrew_locale, format_scheduls, format_task_list, get_sleep_message, render_no_tasks_message, format_schedule_output
from schedule_utils_logic import load_and_filter_schedule, find_current_task_index
from schedule_config import CONFIG

def generate_schedule_display():
    now = datetime.now()
    results = []
    if (msg := get_sleep_message(now)):
        results.append(msg)

    schedule, tasks_to_display, task_list = load_and_filter_schedule(now)
    if not schedule:
        return render_no_tasks_message(now)

    current_task_index = find_current_task_index(tasks_to_display, now)
    results += format_scheduls(tasks_to_display, now, current_task_index)


    #total tasks in the schedule
    total_schedule_tasks = len([t for t, task in schedule if task.strip()])
    shown_tasks = len(tasks_to_display)
    summary_text =  CONFIG["left_padding"] * CONFIG["schedule_summery"]["padding_mul"]
    summary_text += f"{shown_tasks}/{total_schedule_tasks} "
    summary_text += CONFIG["schedule_summery"]["text"]
    from schedule_utils_text_style import wrap_color
    summary_line = wrap_color(summary_text, CONFIG["schedule_summery"]["color"])

    results.append(summary_line)


    if task_list:
        results.append((""))    #space
        results += format_task_list(task_list)





    return format_schedule_output(results, now)

def show_schedule():
    setup_hebrew_locale()
    return generate_schedule_display()

if __name__ == "__main__":
    print(show_schedule())
