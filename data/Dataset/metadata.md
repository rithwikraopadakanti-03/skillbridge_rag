# Dataset Metadata — Student Academic Intelligence System

**Reference Date:** January 15, 2025

## Files

### courses.csv (20 rows)
| Column | Type | Description |
|--------|------|-------------|
| course_id | string | Unique course ID (CRS001–CRS020) |
| course_name | string | Course name |
| total_modules | int | Number of modules in the course |
| total_sessions | int | Total planned sessions |
| passing_grade | int | Minimum grade to pass (50 or 55) |

### mentors.csv (30 rows)
| Column | Type | Description |
|--------|------|-------------|
| mentor_id | string | Unique mentor ID (MNT001–MNT030) |
| mentor_name | string | Full name |
| department | string | Department (Computer Science, Data Science, Full Stack, Foundations, Career Services) |

### students.csv (800 rows)
| Column | Type | Description |
|--------|------|-------------|
| student_id | string | Unique ID (STU0001–STU0800) |
| student_name | string | Full name |
| batch | string | Batch code (BATCH-2023-A/B, BATCH-2024-A/B) |
| course_enrolled | string | FK → courses.course_id |
| enrollment_date | date | ISO format (YYYY-MM-DD) |
| current_module | int | Highest module reached as of reference date |
| mentor_id | string | FK → mentors.mentor_id |

### assessments.csv (~14,000 rows)
| Column | Type | Description |
|--------|------|-------------|
| assessment_id | string | Unique ID (ASM000001+) |
| student_id | string | FK → students.student_id |
| course_id | string | FK → courses.course_id |
| module | int | Module number for this assessment |
| type | string | quiz, assignment, project, or exam |
| max_score | float | Maximum possible score |
| scored | float | Actual score achieved (late penalties already applied) |
| due_date | date | When the assessment was due |
| submitted_date | date | When the student submitted |

### attendance.csv (~18,000 rows)
| Column | Type | Description |
|--------|------|-------------|
| student_id | string | FK → students.student_id |
| date | date | Session date |
| session_type | string | lecture, lab, or mentoring |
| status | string | present, absent, or late |
