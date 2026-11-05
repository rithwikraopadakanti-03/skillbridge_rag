# SkillBridge EdTech — Frequently Asked Questions


## General Questions

**Q: What is the reference date for all calculations?**  
A: All computations (grade calculation, attendance percentage, progress status, alerts) use **January 15, 2025** as the reference date.

**Q: How many batches are there?**  
A: There are four batches: BATCH-2023-A (Jan–Mar 2023), BATCH-2023-B (Jul–Sep 2023), BATCH-2024-A (Jan–Mar 2024), and BATCH-2024-B (Jul–Sep 2024).

**Q: What courses are offered?**  
A: SkillBridge EdTech offers 20 courses covering programming fundamentals, web development, data science, and professional skills. See the courses dataset for details.

## Grading Questions

**Q: What if a student has no project assessments?**  
A: The project component average is treated as 0 (zero). It is NOT excluded from the weighted calculation. This means the student's grade will be lower.

**Q: Are all assessment types equally weighted?**  
A: No. Assignments carry the most weight (30%), followed by Projects and Exams (25% each), then Quizzes (20%).

**Q: How is the grade computed if a student has multiple quizzes?**  
A: All quiz scores are pooled together: sum of all scored values divided by sum of all max_score values, multiplied by 100.

## Attendance Questions

**Q: Do lab sessions count more than lectures?**  
A: Yes. Lab sessions have a weight of 1.5× while lectures and mentoring sessions have a weight of 1.0×. This affects the weighted attendance calculation.

**Q: What does "late" mean for attendance?**  
A: A "late" status counts as 0.5 present (half credit) in all attendance calculations.

**Q: What is the minimum attendance requirement?**  
A: 75% weighted attendance is required. Below 75% triggers counseling; below 60% may result in probation.

## Progress Questions

**Q: How fast should a student progress through modules?**  
A: The expected pace is 1 module every 3 weeks from enrollment date.

**Q: What is "At Risk" status?**  
A: A student more than 3 modules behind expected progress is classified as "At Risk."

## Alert Questions

**Q: Can a student with a high grade still get a Red alert?**  
A: Yes. If their weighted attendance is below 60%, they will be Red regardless of grade.

**Q: What is the difference between Orange and Yellow alerts?**  
A: Yellow is triggered when grade < 65 OR attendance < 70. Orange is the "catch-all" for students who aren't Red or Yellow but don't meet Green criteria (grade ≥ 75 AND attendance ≥ 75).

**Q: How are parent calls prioritized?**  
A: Red = weekly calls (immediate priority), Yellow = bi-weekly (high priority), Orange = monthly (medium), Green = quarterly (optional).

## Data Questions

**Q: What does the "current_module" field in students.csv represent?**  
A: It represents the highest module the student has reached in their enrolled course, as of the reference date.

**Q: Are late submission penalties already applied?**  
A: Yes. The `scored` column in assessments.csv already includes any late penalties. No additional deduction is needed.

**Q: How are mentors assigned?**  
A: Each student is assigned one mentor. A mentor can have multiple students across different courses and batches.
