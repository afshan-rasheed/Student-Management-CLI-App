import csv
import json
import os

JSON_FILE = "students.json"

def get_csv_path():
    """Give the absolute path of the CSV file from the user."""
    file_path = input("Enter CSV file absolute path: ").strip()
    if not os.path.exists(file_path):
        print("File not found! Please enter a valid path.\n")
        return None
    return file_path

def load_students():
    """Loads students from JSON first; if empty, loads from CSV."""
    students = []
    
    if os.path.exists(JSON_FILE) and os.stat(JSON_FILE).st_size > 0:
        try:
            with open(JSON_FILE, "r") as file:
                students = json.load(file)
        except json.JSONDecodeError:
            print("JSON file is corrupt or empty, switching to CSV.")

    return students

def save_student_data(students, file_path):
    save_to_json(students)  # Always update JSON

    #Ensure CSV is updated even if file_path was never set
    if not file_path:
        file_path = "students.csv"  # Default CSV file
    save_csv(file_path, students)


def bonus_1(file_path):
    """Loads student data from a CSV file."""
    students = []
    try:
        with open(file_path, "r", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            students = [row for row in reader]
        save_student_data(students, file_path)  #  Auto-sync JSON when loading CSV
    except Exception as e:
        print(f" Error reading file: {e}")
    return students


def save_to_json(students):
    """Saves student data to JSON file."""
    try:
        with open(JSON_FILE, "w") as file:
            json.dump(students, file, indent=4)
    except Exception as e:
        print(f"Error saving JSON: {e}")

def save_csv(file_path, students):
    """Save the Updated students list into the CSV file"""
    try:
        with open(file_path, "w", newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["ID", "Name", "Roll_no", "Grade"])
            writer.writeheader()
            writer.writerows(students)
    except Exception as e:
        print(f"Error saving CSV: {e}")
        
def bonus_2():
    """Allows runtime file selection and column extraction."""
    file_path = input("Enter CSV file absolute path: ").strip()
    
    # Check if file exists
    if not os.path.exists(file_path):
        print("File not found! Please enter a valid path.\n")
        return
    
    # Ask user which columns they want to extract
    columns = input("Enter column names to extract (comma-separated): ").strip().split(',')
    columns = [col.strip() for col in columns] 

    extracted_data = []

    try:
        with open(file_path, "r", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                filtered_row = {col: row[col] for col in columns if col in row}
                extracted_data.append(filtered_row)
                
        if extracted_data:
            print("\nExtracted Data:")
            for item in extracted_data:
                print(item)
        else:
            print(" No matching columns found in the file.\n")

    except Exception as e:
        print(f"Error reading file: {e}")


def add_student(students, file_path):
    """Adds a new student and updates both JSON & CSV."""
    student_id = input("Enter student ID: ").strip()

    # Check if ID already exists
    if any(student["ID"] == student_id for student in students):
        print("Student ID already exists! Please enter a unique ID.\n")
        return  

    name = input("Enter Name: ")
    roll_no = input("Enter Roll No: ")
    grade = input("Enter Grade: ")

    new_student = {"ID": student_id, "Name": name, "Roll_no": roll_no, "Grade": grade}
    students.append(new_student)

    save_student_data(students, file_path)  
    print(" New student added successfully!\n")

def display_students(students):
    """Displays student data."""
    if not students:
        print("No student data found.\n")
        return

    print("\nStudent Data:")
    print("-" * 50)
    for student in students:
        print(f" ID: {student['ID']} | Name: {student['Name']} | Roll No: {student['Roll_no']} | Grade: {student['Grade']}")
    print("-" * 50)

def search_student(students):
    """Searches for a student by ID."""
    student_id = input("Enter Student ID to search: ").strip()
    found = [s for s in students if s["ID"] == student_id]
    if found:
        print("\nStudent Found:")
        print(found[0])
    else:
        print("Student not found!\n")

def update_student(students, file_path):
    """Updates student data."""
    student_id = input("Enter Student ID to update: ").strip()
    for student in students:
        if student["ID"] == student_id:
            student["Name"] = input(f"Name [{student['Name']}]: ") or student["Name"]
            student["Roll_no"] = input(f"Roll No [{student['Roll_no']}]: ") or student["Roll_no"]
            student["Grade"] = input(f"Grade [{student['Grade']}]: ") or student["Grade"]
            save_student_data(students, file_path)
            print("Student data updated!\n")
            return
    print("Student not found!\n")

def delete_student(students, file_path):
    """Deletes a student by ID."""
    student_id = input("Enter Student ID to delete: ").strip()
    new_students = [s for s in students if s["ID"] != student_id]
    if len(new_students) == len(students):
        print("Student not found!\n")
    else:
        save_student_data(new_students, file_path)
        print("Student deleted!\n")

def menu():
    """CLI menue for user."""
    students = load_students()  
    file_path = "students.csv"  

    while True:
        print("\n=== Student Management CLI App ===")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student by ID")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")
        print("7. Bonus 1: Load External CSV File")   
        print("8. Bonus 2: Extract Specific Columns from CSV")  
        choice = input("Enter your choice (1-8): ").strip()
        print()

        if choice == "1":
            add_student(students, file_path)
        elif choice == "2":
            display_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_student(students, file_path)
        elif choice == "5":
            delete_student(students, file_path)
        elif choice == "6":
            print("Exiting program. Goodbye!")
            break
        elif choice == "7":
            file_path = get_csv_path()  
            if file_path:
                students = bonus_1(file_path) 
                print("Bonus 1: External CSV File Loaded Successfully!\n")
        elif choice == "8":
            bonus_2()  
        else:
            print("Invalid choice! Try again.\n")



# Run the application
if __name__ == "__main__":
    menu()


