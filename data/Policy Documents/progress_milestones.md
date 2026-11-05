# SkillBridge EdTech — Progress Milestones Policy

**Reference Date for All Calculations: January 15, 2025**

## 1. Expected Module Progression

Students are expected to complete **1 module every 3 weeks** from their enrollment date.

```
expected_module = weeks_since_enrollment / 3
```

Where:
```
weeks_since_enrollment = (reference_date - enrollment_date).days / 7
```

The expected module is capped at the course's `total_modules`.

## 2. Progress Status

| Condition                                          | Status       |
|----------------------------------------------------|-------------|
| current_module ≥ expected_module                    | On Track     |
| current_module ≥ expected_module - 1                | Slightly Behind |
| current_module ≥ expected_module - 3                | Behind       |
| current_module < expected_module - 3                | At Risk      |

## 3. Completion Percentage

```
completion_pct = (current_module / total_modules) × 100
```

## 4. Estimated Completion Date

Based on actual pace:

```
weeks_per_module = weeks_since_enrollment / current_module
remaining_modules = total_modules - current_module
remaining_weeks = remaining_modules × weeks_per_module
estimated_completion = reference_date + remaining_weeks (in days)
```

If the student has completed all modules (`current_module == total_modules`), the course is marked as **Completed**.

## 5. Batch-Level Metrics

Batch progress is measured as the average completion percentage across all students in a batch:

```
batch_avg_completion = mean(completion_pct for all students in batch)
```

## 6. Course-Level Metrics

Course progress is measured as the average completion percentage across all students enrolled in that course:

```
course_avg_completion = mean(completion_pct for all students in course)
```
