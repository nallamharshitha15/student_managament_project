USE student_management;

# Students table
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    batch VARCHAR(50) DEFAULT 'Data Analyst'
);

# Attendence table
CREATE TABLE attendance (
    student_id INT PRIMARY KEY,
    total_classes INT DEFAULT 0,
    attended_classes INT DEFAULT 0,
    FOREIGN KEY (student_id)
    REFERENCES students(student_id)
);

# Subjects table
CREATE TABLE subjects (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(50) UNIQUE NOT NULL
);

# Marks table
CREATE TABLE marks (
    student_id INT,
    subject_id INT,
    marks_obtained INT,
    PRIMARY KEY (student_id, subject_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

# To display all tables
SHOW TABLES;

#To check sturcture
DESC students;
DESC attendance;
DESC subjects;
DESC marks;


# Inserting values
# Insert students details

INSERT INTO students
(student_id, student_name, batch)
VALUES
(101, 'Vidya', 'Data Analyst'),
(102, 'Jash', 'Data Analyst'),
(103, 'Rahul', 'Java'),
(104, 'Sneha', 'Data Analyst');


# Insert attendence

INSERT INTO attendance
(student_id, total_classes, attended_classes)
VALUES
(101, 20, 10),
(102, 20, 18),
(103, 20, 14),
(104, 20, 16);

# Insert subjects

INSERT INTO subjects (subject_name)
VALUES
('Python'),
('MySQL'),
('Power BI');


#Insert students marks

INSERT INTO marks VALUES
(101, 1, 60),
(101, 2, 70),
(101, 3, 80),
(102, 1, 80),
(102, 2, 70),
(102, 3, 90),
(103, 1, 45),
(103, 2, 55),
(103, 3, 50),
(104, 1, 90),
(104, 2, 85),
(104, 3, 95);     
      

# To check table records
SELECT * FROM students;
SELECT * FROM attendance;
SELECT * FROM subjects;
SELECT * FROM marks;

DROP TABLE marks;