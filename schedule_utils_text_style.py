# style.py
from schedule_config import CONFIG
from schedule_utils_rtl import reorder_mixed_rtl, reverse_if_hebrew

def wrap_color(text, color=None):
    if not CONFIG["enable_conky_markup"] or not color:
        return text
    return f"${{color {color}}}{text}${{color}}"

def get_style(task, task_time, now, is_current, task_index, current_index):
    if is_current:
        return CONFIG["STYLE_BY_TYPE"]["now"]
    elif task.startswith('[!]'):
        return CONFIG["STYLE_BY_TYPE"]["marked"]
    elif current_index is not None:
        if task_index < current_index:
            return CONFIG["STYLE_BY_TYPE"]["past"]
        elif task_index > current_index:
            return CONFIG["STYLE_BY_TYPE"]["future"]
    elif task_time < now:
        return CONFIG["STYLE_BY_TYPE"]["past"]
    return CONFIG["STYLE_BY_TYPE"]["future"]

def format_schedule_line(task_time, task, style):
    prefix = style.get("prefix", "")
    color = style.get("color")
    if task.startswith('[!]'):
        task = task.replace('[!]', '', 1).strip()
    line = f"{prefix} {task_time.strftime('%H:%M')}  {reorder_mixed_rtl(task)}"
    return wrap_color(line, color)

def format_scheduls(tasks_to_display, now, current_task_index):
    return [
        format_schedule_line(t, task, get_style(task, t, now, i == current_task_index, i, current_task_index))
        for i, (t, task) in enumerate(tasks_to_display)
    ]

def format_task_list(task_list, color="white"):
    results = []
    title = CONFIG.get("task_list_header_title", None)
    if title:
        title_line = CONFIG.get("left_padding", "")
        title_line += reverse_if_hebrew(title)
        results.append(wrap_color(title_line, color))

    for line in task_list:
        formatted = CONFIG.get("short_left_padding", "")
        formatted += reorder_mixed_rtl(line.strip())
        results.append(wrap_color(formatted, color))
    
    return results