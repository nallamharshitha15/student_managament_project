USE student_management;

# Display student names and IDs
SELECT student_id, student_name
FROM students;

# Calculate attendance percentage
SELECT student_id,
ROUND((attended_classes / total_classes) * 100, 2) AS percentage
FROM attendance;

# Find students below 75% attendance
SELECT student_id, 
ROUND((attended_classes / total_classes) * 100, 2) AS percentage
FROM attendance
WHERE (attended_classes / total_classes) * 100 < 75;

# Calculate total marks
SELECT student_id, SUM(marks_obtained) AS total
FROM marks
GROUP BY student_id;

# Calculate average marks
SELECT student_id, AVG(marks_obtained) AS average
FROM marks
GROUP BY student_id;

# students scoring below 60 average
SELECT student_id, AVG(marks_obtained) AS average
FROM marks
GROUP BY student_id
HAVING AVG(marks_obtained) < 60;

# Highest marks
SELECT MAX(marks_obtained) FROM marks;

# Lowest marks
SELECT MIN(marks_obtained) FROM marks;

# Count total students
SELECT COUNT(*) FROM students;

#Display student names with their attendance details
SELECT s.student_name, a.total_classes, a.attended_classes
FROM students s
JOIN attendance a
ON s.student_id = a.student_id;

#Display student names with attendance percentage
SELECT s.student_name,
ROUND((a.attended_classes / a.total_classes) * 100, 2) AS percentage
FROM students s
JOIN attendance a
ON s.student_id = a.student_id;

#Display student names with subject names and marks
SELECT s.student_name, sub.subject_name, m.marks_obtained
FROM students s
JOIN marks m ON s.student_id = m.student_id
JOIN subjects sub ON m.subject_id = sub.subject_id;

#Display student names with total marks
SELECT s.student_name, SUM(m.marks_obtained) AS total
FROM students s
JOIN marks m ON s.student_id = m.student_id
GROUP BY s.student_name;

# Assign performance categories
SELECT student_id,
AVG(marks_obtained) AS average,
CASE
    WHEN AVG(marks_obtained) >= 90 THEN 'Excellent'
    WHEN AVG(marks_obtained) >= 75 THEN 'Very Good'
    WHEN AVG(marks_obtained) >= 60 THEN 'Good'
    WHEN AVG(marks_obtained) >= 40 THEN 'Average'
    ELSE 'Poor'
END AS performance
FROM marks
GROUP BY student_id;

select * from students;
