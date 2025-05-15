
import platform

CONFIG = {
    "SCHEDULE_FILE": "/home/arthur/schedule/schedule.csv",
    "no_tasks_message": "אין משימות בקובץ",
    "header_title": "משימות:",
    "header_title_padding_mul": 2,
    "date_line_padding_mul": 3,
    "task_list_header_title": "משימות:",
    "left_padding": "   ",
    "short_left_padding": "  ",
    "schedule_summery":{
        "color" : "gray",
        "text" : "tasks",
        "padding_mul": 6
    },
    "sleep_block": {
        "enabled": True,
        "hours": [23, 7],
        "message": "******* Sleep Time ****",
        "color": "red"
    },
    "STYLE_BY_TYPE": {
        "now":    {"prefix": " • ",  "color": "green"},
        "past":   {"prefix": "    ", "color": "gray"},
        "future": {"prefix": "    ", "color": "white"},
        "marked": {"prefix": "    ", "color": "orange"},
    },
    "enable_conky_markup": platform.system() == "Linux"
}