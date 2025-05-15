# ui_render.py
from schedule_config import CONFIG
from schedule_utils_rtl import reverse_if_hebrew, setup_hebrew_locale
from schedule_utils_text_style import format_scheduls, wrap_color, format_task_list

__all__ = ["setup_hebrew_locale", "format_scheduls", "format_task_list", "get_sleep_message", "render_no_tasks_message", "format_schedule_output"]


def get_sleep_message(now):
    block = CONFIG.get("sleep_block", {})
    if not block.get("enabled"):
        return None
    from_hour, to_hour = block.get("hours", [23, 7])
    if from_hour <= now.hour or now.hour < to_hour:
        return CONFIG["left_padding"] + wrap_color(block.get("message", ""), block.get("color"))
    return None

def render_no_tasks_message(now):
    header = CONFIG["left_padding"] * CONFIG["header_title_padding_mul"] + reverse_if_hebrew(CONFIG["header_title"])
    date_line = CONFIG["left_padding"] * CONFIG["date_line_padding_mul"] + reverse_if_hebrew(now.strftime('%A')) + " " + now.strftime('%d.%m.%Y')
    return f"{header}\n{date_line}\n\n" + reverse_if_hebrew(CONFIG["no_tasks_message"])

def format_schedule_output(results, now):
    header = CONFIG["left_padding"]  * CONFIG["header_title_padding_mul"] + reverse_if_hebrew(CONFIG["header_title"])
    date_line = CONFIG["left_padding"] * CONFIG["date_line_padding_mul"] + reverse_if_hebrew(now.strftime('%A')) + " " + now.strftime('%d.%m.%Y')
    return f"{header}\n{date_line}  {now.strftime('%H:%M')}\n\n" + "\n".join(results)
