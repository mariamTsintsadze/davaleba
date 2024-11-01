import csv
from statistics import mean

file_path = 'students.csv'

def add_student(id, name, age, grade, subject_name, mark):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)
    
    existing_ids = {row[0] for row in data[1:]} 
    if str(id) in existing_ids:
        print(f"Student with ID {id} already exists.")
        return
    
    data.append([id, name, age, grade, subject_name, mark])
    
    header, rows = data[0], data[1:]
    rows = sorted(rows, key=lambda row: int(row[0]))
    
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)

def read_student_data(student_id=None):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        students = list(reader)
        
        if student_id:
            student_data = [row for row in students if row[0] == str(student_id)]
            return [header] + student_data if student_data else "Student not found."
        else:
            return [header] + students

def calculate_average_mark():
    subject_marks = {}
    
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader) 

        for row in reader:
            subject_name = row[4]
            mark = int(row[5])
            if subject_name in subject_marks:
                subject_marks[subject_name].append(mark)
            else:
                subject_marks[subject_name] = [mark]
    
    averages = {subject: mean(marks) for subject, marks in subject_marks.items()}
    return averages

def update_student_mark(student_id, subject_name, new_mark):
    updated = False
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)
        
        for row in rows:
            if row[0] == str(student_id) and row[4] == subject_name:
                row[5] = str(new_mark)
                updated = True
                break
    
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    
    return "Student mark updated successfully." if updated else "Student or subject not found."

def create_csv_file():
    try:
        with open(file_path, mode='x', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["id", "name", "age", "grade", "subject_name", "mark"])
    except FileExistsError:
        print("File already exists.")



create_csv_file()

add_student(1, 'Alice', 20, 'A', 'Math', 85)
add_student(2, 'Bob', 22, 'B', 'Science', 90)

print("All students:", read_student_data())

print("Student ID 1:", read_student_data(1))

print("Average marks by subject:", calculate_average_mark())

print(update_student_mark(1, 'Math', 95))
