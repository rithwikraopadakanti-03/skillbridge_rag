# SkillBridge EdTech — Grading Policy


## 1. Assessment Components and Weights

Every course uses the following four assessment types with fixed weights:

| Component   | Weight | Description                                  |
|-------------|--------|----------------------------------------------|
| Quizzes     | 20%    | Module-level MCQ and short-answer tests       |
| Assignments | 30%    | Coding tasks and written submissions          |
| Projects    | 25%    | Hands-on projects assessed every 3 modules    |
| Exams       | 25%    | Mid-term and end-term examinations            |

## 2. Grade Calculation Formula

The **overall grade** for a student in a course is calculated as:

```
grade = (quiz_avg × 0.20) + (assignment_avg × 0.30) + (project_avg × 0.25) + (exam_avg × 0.25)
```

Where each component average is computed as:

```
component_avg = (sum of scored / sum of max_score) × 100
```

For example, if a student has quiz scores of 18/25 and 20/25:
- quiz_avg = ((18 + 20) / (25 + 25)) × 100 = 76.0

**Important:** If a student has no assessments of a particular type, that component average is treated as **0** (zero), NOT excluded from the calculation.

## 3. Passing Criteria

- Each course has a **passing_grade** defined in the course catalog (typically 50 or 55).
- A student **passes** if their overall grade ≥ the course's passing_grade.
- A student **fails** if their overall grade < the course's passing_grade.

## 4. Letter Grade Mapping

| Grade Range | Letter Grade | Status         |
|-------------|-------------|----------------|
| 90 – 100   | A+          | Distinction    |
| 80 – 89.99 | A           | Excellent      |
| 70 – 79.99 | B           | Good           |
| 60 – 69.99 | C           | Average        |
| 50 – 59.99 | D           | Below Average  |
| 0 – 49.99  | F           | Fail           |

## 5. Reverse Grade Computation

To determine the **minimum exam score** a student needs to achieve the passing grade:

```
min_exam_score = (passing_grade - (quiz_avg × 0.20 + assignment_avg × 0.30 + project_avg × 0.25)) / 0.25
```

If the result exceeds 100, the student **cannot pass** with exams alone. If the result is ≤ 0, the student has **already passed** regardless of exam performance.

## 6. Late Submission Policy

Assessments submitted after the due date receive the following penalties:
- 1–3 days late: **10% deduction** from scored marks
- 4–7 days late: **25% deduction** from scored marks
- More than 7 days late: **50% deduction** from scored marks

**Note:** In the current dataset, late penalties are already factored into the `scored` column. No additional penalty calculation is needed when computing grades.
