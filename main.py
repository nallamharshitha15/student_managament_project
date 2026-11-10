
import mysql.connector
from database import get_connection


# ---------- INPUT FUNCTION ----------
def get_integer(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Please enter a valid number.")


# ---------- ADD STUDENT ----------
def add_student():
    sid = get_integer("Enter Student ID: ")
    name = input("Enter Student Name: ").strip()

    if not name or not name.replace(" ", "").isalpha():
        print("Invalid name!")
        return

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO students (student_id, student_name, batch)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (sid, name, "Data Analyst"))
        connection.commit()

        print("Student added successfully!")

    except mysql.connector.IntegrityError:
        print("Student ID already exists!")

    except mysql.connector.Error as error:
        print("Database error:", error)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()


# ---------- SELECT STUDENT ----------
def select_student():
    choice = input("Search by 1.ID or 2.Name: ")

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        if choice == "1":
            sid = get_integer("Enter Student ID: ")

            cursor.execute(
                "SELECT * FROM students WHERE student_id = %s",
                (sid,)
            )

            student = cursor.fetchone()

            if student:
                print("Student Found:", student)
                return student[0]

        elif choice == "2":
            name = input("Enter Student Name: ").strip()

            cursor.execute(
                """SELECT * FROM students
                   WHERE LOWER(student_name) = LOWER(%s)""",
                (name,)
            )

            students = cursor.fetchall()

            if len(students) == 1:
                print("Student Found:", students[0])
                return students[0][0]

            elif len(students) > 1:
                print("Multiple students found:")

                for student in students:
                    print(student)

                sid = get_integer("Enter Student ID: ")

                for student in students:
                    if student[0] == sid:
                        return sid

        else:
            print("Invalid selection!")
            return None

        print("Student not found!")
        return None

    except mysql.connector.Error as error:
        print("Database error:", error)
        return None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ---------- ATTENDANCE ----------
def attendance(sid):
    total = get_integer("Total classes conducted: ")
    attended = get_integer("Classes attended: ")

    if total <= 0 or attended < 0 or attended > total:
        print("Invalid attendance details!")
        return

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO attendance
        (student_id, total_classes, attended_classes)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
        total_classes = VALUES(total_classes),
        attended_classes = VALUES(attended_classes)
        """

        cursor.execute(query, (sid, total, attended))
        connection.commit()

        percentage = attended / total * 100

        print(f"Attendance: {percentage:.2f}%")
        print("Attendance saved successfully!")

    except mysql.connector.Error as error:
        print("Database error:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ---------- ATTENDANCE PERCENTAGE ----------
def attendance_percentage(sid):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT total_classes, attended_classes
        FROM attendance
        WHERE student_id = %s
        """

        cursor.execute(query, (sid,))
        data = cursor.fetchone()

        if data is None:
            print("Attendance not recorded!")
            return

        total, attended = data
        absent = total - attended
        percentage = attended / total * 100

        print("\nAttendance Details")
        print("Total Classes:", total)
        print("Attended:", attended)
        print("Absent:", absent)
        print(f"Percentage: {percentage:.2f}%")

    except mysql.connector.Error as error:
        print("Database error:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ---------- SUBJECT MARKS ----------
def subject_marks(sid):
    connection = None
    cursor = None

    try:
        marks = {}

        for subject in ["Python", "MySQL", "Power BI"]:
            while True:
                value = get_integer(f"Enter {subject} marks: ")

                if 0 <= value <= 100:
                    marks[subject] = value
                    break

                print("Marks must be between 0 and 100.")

        connection = get_connection()
        cursor = connection.cursor()

        for subject, value in marks.items():

            cursor.execute(
                "SELECT subject_id FROM subjects WHERE subject_name = %s",
                (subject,)
            )

            result = cursor.fetchone()

            if result is None:
                print(subject, "not found in subjects table!")
                return

            subject_id = result[0]

            query = """
            INSERT INTO marks
            (student_id, subject_id, marks_obtained)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
            marks_obtained = VALUES(marks_obtained)
            """

            cursor.execute(query, (sid, subject_id, value))

        connection.commit()
        print("Marks saved successfully!")

    except mysql.connector.Error as error:
        if connection:
            connection.rollback()
        print("Database error:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ---------- GET MARKS ----------
def get_marks(sid):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT sub.subject_name, m.marks_obtained
        FROM marks m
        JOIN subjects sub
        ON m.subject_id = sub.subject_id
        WHERE m.student_id = %s
        """

        cursor.execute(query, (sid,))
        return cursor.fetchall()

    except mysql.connector.Error as error:
        print("Database error:", error)
        return None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ---------- PERFORMANCE ----------
def performance(sid):
    data = get_marks(sid)

    if not data:
        print("Marks not entered!")
        return

    marks = dict(data)

    if len(marks) < 3:
        print("Enter marks for all three subjects!")
        return

    total = sum(marks.values())
    average = total / 3

    print("\nSubject Performance")

    for subject, value in marks.items():
        print(f"{subject}: {value}/100")

    print("\nTotal:", total, "/300")
    print(f"Average: {average:.2f}%")

    print("Highest Marks:", max(marks.values()))
    print("Lowest Marks:", min(marks.values()))

    if average >= 90:
        category = "Excellent"
    elif average >= 75:
        category = "Very Good"
    elif average >= 60:
        category = "Good"
    elif average >= 40:
        category = "Average"
    else:
        category = "Poor"

    print("Category:", category)


# ---------- LOW ATTENDANCE ----------
def low_attendance():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT s.student_id, s.student_name,
        a.total_classes, a.attended_classes
        FROM students s
        JOIN attendance a
        ON s.student_id = a.student_id
        """

        cursor.execute(query)
        students = cursor.fetchall()

        print("\nStudents Below 75% Attendance")

        found = False

        for student in students:
            sid, name, total, attended = student
            percentage = attended / total * 100

            if percentage < 75:
                found = True
                print(f"{sid} | {name} | {percentage:.2f}%")

        if not found:
            print("No students found!")

    except mysql.connector.Error as error:
        print("Database error:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ---------- LOW PERFORMANCE ----------
def low_performance():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT s.student_id, s.student_name,
        AVG(m.marks_obtained) AS average
        FROM students s
        JOIN marks m
        ON s.student_id = m.student_id
        GROUP BY s.student_id, s.student_name
        HAVING COUNT(m.subject_id) = 3
        AND AVG(m.marks_obtained) < 50
        """

        cursor.execute(query)
        students = cursor.fetchall()

        print("\nStudents with Average Below 50%")

        if not students:
            print("No students found!")
            return

        for student in students:
            print(
                student[0],
                student[1],
                f"{student[2]:.2f}%"
            )

    except mysql.connector.Error as error:
        print("Database error:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ---------- RANKING ----------
def ranking():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT s.student_id, s.student_name,
        SUM(m.marks_obtained) AS total,
        AVG(m.marks_obtained) AS average
        FROM students s
        JOIN marks m
        ON s.student_id = m.student_id
        GROUP BY s.student_id, s.student_name
        HAVING COUNT(m.subject_id) = 3
        ORDER BY average DESC
        """

        cursor.execute(query)
        students = cursor.fetchall()

        print("\nStudent Ranking")

        if not students:
            print("No complete marks available!")
            return

        for rank, student in enumerate(students, start=1):
            print(
                f"Rank {rank} | ID: {student[0]} | "
                f"Name: {student[1]} | "
                f"Total: {student[2]}/300 | "
                f"Average: {student[3]:.2f}%"
            )

    except mysql.connector.Error as error:
        print("Database error:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ---------- SAVE REPORT ----------
def save_report(sid):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE student_id = %s",
            (sid,)
        )
        student = cursor.fetchone()

        if not student:
            print("Student not found!")
            return

        cursor.execute(
            """SELECT total_classes, attended_classes
               FROM attendance WHERE student_id = %s""",
            (sid,)
        )
        attendance_data = cursor.fetchone()

        marks_data = get_marks(sid)

        report = "STUDENT ATTENDANCE & PERFORMANCE REPORT\n"
        report += "========================================\n"
        report += f"Student ID: {student[0]}\n"
        report += f"Name: {student[1]}\n"
        report += f"Batch: {student[2]}\n"

        report += "\nATTENDANCE DETAILS\n"

        if attendance_data:
            total, attended = attendance_data
            percentage = attended / total * 100
            report += f"Total Classes: {total}\n"
            report += f"Attended: {attended}\n"
            report += f"Absent: {total - attended}\n"
            report += f"Percentage: {percentage:.2f}%\n"
        else:
            report += "Attendance not recorded.\n"

        report += "\nSUBJECT MARKS\n"

        if marks_data:
            total_marks = 0

            for subject, value in marks_data:
                report += f"{subject}: {value}/100\n"
                total_marks += value

            if len(marks_data) == 3:
                average = total_marks / 3
                report += f"Total: {total_marks}/300\n"
                report += f"Average: {average:.2f}%\n"
        else:
            report += "Marks not recorded.\n"

        filename = f"student_{sid}_report.txt"

        with open(filename, "w") as file:
            file.write(report)

        print("Report saved as", filename)

    except mysql.connector.Error as error:
        print("Database error:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ---------- MAIN MENU ----------
while True:
    print("\n===================================")
    print("       DATA ANALYST BATCH")
    print(" STUDENT ATTENDANCE & PERFORMANCE")
    print("===================================")

    print("1. Add Student")
    print("2. Select Student")
    print("3. Attendance")
    print("4. Attendance Percentage")
    print("5. Subject Marks")
    print("6. Performance")
    print("7. Low Attendance Students")
    print("8. Low Performance Students")
    print("9. Student Ranking")
    print("10. Save Student Report")
    print("11. Exit")

    choice = input("\nEnter choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        sid = select_student()
        if sid is not None:
            print("Selected Student ID:", sid)

    elif choice in ["3", "4", "5", "6", "10"]:
        sid = select_student()

        if sid is not None:
            if choice == "3":
                attendance(sid)
            elif choice == "4":
                attendance_percentage(sid)
            elif choice == "5":
                subject_marks(sid)
            elif choice == "6":
                performance(sid)
            elif choice == "10":
                save_report(sid)

    elif choice == "7":
        low_attendance()

    elif choice == "8":
        low_performance()

    elif choice == "9":
        ranking()

    elif choice == "11":
        print("System closed.")
        break

    else:
        print("Invalid choice!")
