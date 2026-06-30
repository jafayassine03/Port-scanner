import json
import os

FILE_NAME = "academictracker.json"


def ensure_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w") as f:
            json.dump({}, f)


def load_data():
    ensure_file()
    with open(FILE_NAME, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)


students = load_data()


def add_student():
    name = input("Enter student name: ").strip()

    if name in students:
        print("Student already exists!")
        return

    try:
        age = int(input("Enter student age: "))
        grade = float(input("Enter student grade: "))
    except ValueError:
        print("Age must be number and grade must be numeric!")
        return

    major = input("Enter student major: ")
    note = input("Enter student note: ")

    students[name] = {
        "age": age,
        "grade": grade,
        "major": major,
        "note": note
    }

    save_data(students)
    print("Student added successfully!")


def view_students():
    if not students:
        print("No students found.")
        return

    for name, info in students.items():
        print("-" * 30)
        print(f"Name  : {name}")
        print(f"Age   : {info['age']}")
        print(f"Grade : {info['grade']}")
        print(f"Major : {info['major']}")
        print(f"Note  : {info['note']}")
    print("-" * 30)


def edit_student():
    name = input("Enter student name to edit: ").strip()

    if name not in students:
        print("Student not found!")
        return

    print("What would you like to edit?")
    print("1. Age")
    print("2. Grade")
    print("3. Major")
    print("4. Note")

    try:
        choice = int(input("Enter your choice: "))

        if choice == 1:
            students[name]["age"] = int(input("Enter new age: "))

        elif choice == 2:
            students[name]["grade"] = float(input("Enter new grade: "))

        elif choice == 3:
            students[name]["major"] = input("Enter new major: ")

        elif choice == 4:
            students[name]["note"] = input("Enter new note: ")

        else:
            print("Invalid choice.")
            return

        save_data(students)
        print(f"{name}'s information updated successfully!")

    except ValueError:
        print("Invalid input.")


def delete_student():
    name = input("Enter student name to delete: ").strip()

    if name not in students:
        print("Student not found!")
        return

    del students[name]
    save_data(students)

    print(f"{name} has been deleted.")


def search_student():
    name = input("Enter student name to search: ").strip()

    if name in students:
        info = students[name]

        print("-" * 30)
        print(f"Name  : {name}")
        print(f"Age   : {info['age']}")
        print(f"Grade : {info['grade']}")
        print(f"Major : {info['major']}")
        print(f"Note  : {info['note']}")
        print("-" * 30)

    else:
        print("Student not found!")


def sort_students_by_grade():
    if not students:
        print("No students found.")
        return

    sorted_students = sorted(
        students.items(),
        key=lambda x: x[1]["grade"],
        reverse=True
    )

    for name, info in sorted_students:
        print("-" * 30)
        print(f"Name  : {name}")
        print(f"Grade : {info['grade']}")
    print("-" * 30)


def calculate_average_grade():
    if not students:
        print("No students found.")
        return

    total = sum(student["grade"] for student in students.values())
    average = total / len(students)

    print(f"Average Grade: {average:.2f}")


def top_student():
    if not students:
        print("No students found.")
        return

    name, info = max(
        students.items(),
        key=lambda x: x[1]["grade"]
    )

    print("\nTop Student")
    print("-" * 30)
    print(f"Name  : {name}")
    print(f"Age   : {info['age']}")
    print(f"Grade : {info['grade']}")
    print(f"Major : {info['major']}")
    print(f"Note  : {info['note']}")
    print("-" * 30)


def lowest_student():
    if not students:
        print("No students found.")
        return

    name, info = min(
        students.items(),
        key=lambda x: x[1]["grade"]
    )

    print("\nLowest Student")
    print("-" * 30)
    print(f"Name  : {name}")
    print(f"Age   : {info['age']}")
    print(f"Grade : {info['grade']}")
    print(f"Major : {info['major']}")
    print(f"Note  : {info['note']}")
    print("-" * 30)


def student_statistics():
    if not students:
        print("No students found.")
        return

    grades = [student["grade"] for student in students.values()]

    highest = max(grades)
    lowest = min(grades)
    average = sum(grades) / len(grades)

    print("\nStudent Statistics")
    print("-" * 30)
    print(f"Total Students : {len(students)}")
    print(f"Highest Grade  : {highest}")
    print(f"Lowest Grade   : {lowest}")
    print(f"Average Grade  : {average:.2f}")
    print("-" * 30)


def grade_status():
    if not students:
        print("No students found.")
        return

    print("\nStudent Grade Status")
    print("-" * 30)

    for name, info in students.items():
        grade = info["grade"]

        if grade >= 90:
            status = "Excellent"
        elif grade >= 75:
            status = "Good"
        elif grade >= 50:
            status = "Average"
        else:
            status = "Fail"

        print(f"{name} -> {status}")

    print("-" * 30)


# New Feature: List Students by Major
def list_students_by_major():
    if not students:
        print("No students found.")
        return

    majors = {}
    for name, info in students.items():
        major = info["major"]
        if major not in majors:
            majors[major] = []
        majors[major].append(name)

    print("\nStudents by Major")
    print("-" * 30)
    for major, names in majors.items():
        print(f"Major: {major}")
        for n in names:
            print(f"  - {n}")
    print("-" * 30)


# Main Menu Loop
while True:
    print("\n" + "=" * 10 + " Academic Tracker " + "=" * 10)
    print("1. Add Student")
    print("2. View Students")
    print("3. Edit Student")
    print("4. Delete Student")
    print("5. Search Student")
    print("6. Sort Students by Grade")
    print("7. Calculate Average Grade")
    print("8. Top Student Report")
    print("9. Lowest Student Report")
    print("10. Student Statistics")
    print("11. Grade Status")
    print("13. List Students by Major")  # NEW FEATURE
    print("12. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()
    elif choice == "2":
        view_students()
    elif choice == "3":
        edit_student()
    elif choice == "4":
        delete_student()
    elif choice == "5":
        search_student()
    elif choice == "6":
        sort_students_by_grade()
    elif choice == "7":
        calculate_average_grade()
    elif choice == "8":
        top_student()
    elif choice == "9":
        lowest_student()
    elif choice == "10":
        student_statistics()
    elif choice == "11":
        grade_status()
    elif choice == "13":
        list_students_by_major()  # call new feature
    elif choice == "12":
        print("Exiting...")
        break
    else:
        print("Invalid choice.")