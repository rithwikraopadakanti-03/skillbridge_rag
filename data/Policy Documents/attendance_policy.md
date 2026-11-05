# SkillBridge EdTech — Attendance Policy


## 1. Attendance Tracking

Attendance is recorded for every scheduled session. Each record includes:
- **student_id**: The student
- **date**: Session date
- **session_type**: One of `lecture`, `lab`, or `mentoring`
- **status**: One of `present`, `absent`, or `late`

## 2. Attendance Percentage Formula

The attendance percentage is calculated as:

```
attendance_pct = ((present_count + 0.5 × late_count) / total_sessions) × 100
```

Where:
- `present_count` = number of sessions with status "present"
- `late_count` = number of sessions with status "late"
- `total_sessions` = total number of attendance records for that student

**A "late" counts as half a present (0.5 credit).**

## 3. Lab Session Weighting

Lab sessions are weighted **1.5×** compared to lectures and mentoring sessions.

The **weighted attendance** formula is:

```
weighted_present = Σ (present sessions weight) + 0.5 × Σ (late sessions weight)
weighted_total = Σ (all sessions weight)

Where weight = 1.5 for lab sessions, 1.0 for lecture and mentoring sessions

weighted_attendance_pct = (weighted_present / weighted_total) × 100
```

**Example:**
A student with 10 lectures (8 present, 1 late, 1 absent) and 5 labs (3 present, 1 late, 1 absent):
- weighted_present = (8×1.0 + 3×1.5) + 0.5×(1×1.0 + 1×1.5) = 8 + 4.5 + 0.5 + 0.75 = 13.75
- weighted_total = 10×1.0 + 5×1.5 = 10 + 7.5 = 17.5
- weighted_attendance_pct = (13.75 / 17.5) × 100 = 78.57%

## 4. Minimum Attendance Requirement

- **75%** overall weighted attendance is mandatory.
- Students below 75% are flagged for attendance counseling.
- Students below 60% may be placed on academic probation.

## 5. Attendance by Session Type

Separate attendance percentages can be computed per session type:

```
lecture_attendance = ((lecture_present + 0.5 × lecture_late) / total_lectures) × 100
lab_attendance = ((lab_present + 0.5 × lab_late) / total_labs) × 100
mentoring_attendance = ((mentoring_present + 0.5 × mentoring_late) / total_mentoring) × 100
```

## 6. Monthly Attendance

Attendance can be filtered by month. Monthly attendance uses the same formula but only counts records within the specified month.
