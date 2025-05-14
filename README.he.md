# ווידג'ט משימות בעברית עם Conky

פרויקט זה מציג רשימת משימות מתעדכנת על שולחן העבודה עם תמיכה בעברית ובכיוון ימין-לשמאל (RTL), כולל סימון צבעוני של משימות וטעינה דינמית מקובץ CSV.

![schedule app](./schedule.png)

---

## 📁 מבנה הפרויקט

```
.
├── conky.conf                # קובץ ההגדרות של Conky
├── run.sh                   # סקריפט להרצה ידנית
├── startup_conky.sh         # סקריפט להרצה אוטומטית עם עליית המערכת
├── schedule.csv             # קובץ המשימות היומי
├── schedule_widget.py       # קובץ ראשי
├── schedule_config.py       # הגדרות קבועות
├── schedule_utils_rtl.py    # עיבוד טקסט בעברית ו-RTL
├── schedule_utils_logic.py  # טעינת לוח זמנים ולוגיקה
├── schedule_utils_text_style.py  # עיצוב תצוגת משימות
├── schedule_utils_ui_render.py   # הצגת תוצאה ותאריך
```

---

## 🧰 התקנה

```bash
sudo apt update
sudo apt install conky
```

---

## ▶️ הרצה

כדי להריץ את הווידג'ט ידנית:
```bash
pkill -x conky; sleep 1 && LANG=he_IL.UTF-8 conky -c ./conky.conf &
```

או באמצעות הסקריפט:
```bash
./run.sh
```

---

## 📋 פורמט קובץ CSV

```csv
time,task
08:00,להתחיל את היום
10:00,[!] פגישה חשובה
12:00,ארוחת צהריים
14:00,בדיקת קוד
```

> משימות עם `[!]` יסומנו כמשימות חשובות (בכתום).

---

## 🚀 הרצה אוטומטית עם אתחול

1. פתח את "תוכניות הפעלה עם אתחול"
2. לחץ "הוסף"
3. שם: `Conky Schedule`
4. פקודה: `/path/to/startup_conky.sh`
5. שמור והפעל מחדש


---

## 👤 אודות היוצר

פותח על ידי Arthur (מפתח קוד פתוח, חובב Conky ו-Python)

---

## ⚖️ זכויות שימוש

הפרויקט ניתן לשימוש חופשי.  
**ללא אחריות על נזקים או תקלות בשימוש.**