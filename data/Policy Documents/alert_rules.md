# SkillBridge EdTech — Student Alert Rules


## 1. Alert Classification

Each student is assigned an alert color based on their **grade** and **weighted attendance percentage**.

### Color Thresholds

| Alert Color | Condition                                                         |
|------------|-------------------------------------------------------------------|
| **Red**    | grade < 50 **OR** weighted_attendance_pct < 60                    |
| **Yellow** | grade < 65 **OR** weighted_attendance_pct < 70 (and not Red)      |
| **Green**  | grade ≥ 75 **AND** weighted_attendance_pct ≥ 75                   |
| **Orange** | Everything else (not Red, not Yellow, not Green)                   |

### Evaluation Order (IMPORTANT)

Alerts are evaluated in this **strict priority order**:
1. Check Red conditions first — if ANY Red condition is true → **Red**
2. Check Yellow conditions — if ANY Yellow condition is true → **Yellow**
3. Check Green conditions — if ALL Green conditions are true → **Green**
4. Otherwise → **Orange**

## 2. Alert Formulas

The grade and attendance used in alert calculation are:

- **grade**: Computed per the Grading Policy (quiz_avg×0.20 + assignment_avg×0.30 + project_avg×0.25 + exam_avg×0.25)
- **weighted_attendance_pct**: Computed per the Attendance Policy (with lab=1.5× weight, late=0.5 credit)

## 3. Parent Call Priority

Based on alert color, parent calls are prioritized:

| Alert Color | Call Priority | Call Frequency      |
|------------|---------------|---------------------|
| Red        | Immediate     | Weekly              |
| Yellow     | High          | Bi-weekly           |
| Orange     | Medium        | Monthly             |
| Green      | Low           | Quarterly (optional)|

## 4. Parent Call Triggers

A parent call is **automatically triggered** when:
- A student's alert status changes from Green/Orange to Yellow or Red
- A student misses 3 consecutive sessions
- A student fails any exam (scored < 50% of max_score)
- A student's grade drops more than 10 points in a month

## 5. Batch Alert Summary

For reporting, each batch's alert distribution is:
```
batch_red_count = count of Red students in batch
batch_yellow_count = count of Yellow students in batch
batch_orange_count = count of Orange students in batch
batch_green_count = count of Green students in batch
batch_red_pct = (batch_red_count / total_students_in_batch) × 100
```
