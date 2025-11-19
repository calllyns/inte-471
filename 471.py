# Value object for grades
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Grade:
    course_code: str
    value: str
    
    def get_points(self) -> int:
        mapping = {"A": 4, "B": 3, "C": 2, "D": 1, "F": 0}
        return mapping.get(self.value, 0)

# New high-cohesion class
class AcademicRecord:
    def __init__(self):
        self.grades: Dict[str, Grade] = {}
        self.attendance: Dict[str, List[bool]] = {}
    
    def record_grade(self, course_code: str, grade: str):
        self.grades[course_code] = Grade(course_code, grade)
    
    def record_attendance(self, course_code: str, present: bool):
        self.attendance.setdefault(course_code, []).append(present)
    
    def calculate_gpa(self) -> float:
        if not self.grades:
            return 0.0
        total_points = sum(g.get_points() for g in self.grades.values())
        return round(total_points / len(self.grades), 2)
    
    def calculate_avg_attendance(self) -> float:
        if not self.attendance:
            return 0.0
        total_rate = 0
        for records in self.attendance.values():
            if records:
                total_rate += (sum(records) / len(records)) * 100
        return round(total_rate / len(self.attendance), 1) if self.attendance else 0.0
    
    def generate_performance_report(self):
        gpa = self.calculate_gpa()
        attendance = self.calculate_avg_attendance()
        print(f"GPA: {gpa}, Average Attendance: {attendance}%")
        if gpa >= 3.5 and attendance >= 90:
            print("Excellent performance!")
        elif gpa < 2.0 or attendance < 60:
            print("Warning: Poor performance")
        return gpa

# Refactored Student – now focused only on identity + registration
class Student(Person):
    def __init__(self, student_id: str, name: str, email: str, phone=None):
        super().__init__(student_id, name, email, phone)
        self.role = "Student"
        self.enrolled_courses: List[Course] = []
        self.academic_record = AcademicRecord()  # Composition
    
    def register_course(self, course: 'Course'):
        if course not in self.enrolled_courses:
            self.enrolled_courses.append(course)
            course.enroll_student(self)
            print(f"{self.name} registered for {course.title}")
    
    def show_performance(self):
        self.academic_record.generate_performance_report()

# Course now handles enrollment cleanly
class Course:
    def __init__(self, code: str, title: str, credit_hours: int, lecturer=None):
        self.code = code
        self.title = title
        self.credit_hours = credit_hours
        self.lecturer = lecturer
        self.students: List[Student] = []
    
    def enroll_student(self, student: Student):
        if student not in self.students:
            self.students.append(student)
            student.enrolled_courses.append(self)
    
    def display_details(self):
        print(f"{self.code}: {self.title} ({self.credit_hours} credits)")
        print(f"Lecturer: {self.lecturer.name if self.lecturer else 'TBA'}")
        print(f"Enrolled ({len(self.students)}): {', '.join(s.name for s in self.students)}")

# Registrar now only manages collections – no business logic
class Registrar:
    def __init__(self):
        self.students: List[Student] = []
        self.courses: List[Course] = []
        self.lecturers: List[Lecturer] = []
    
    def add_student(self, student: Student): self.students.append(student)
    def add_course(self, course: Course): self.courses.append(course)
    def add_lecturer(self, lecturer: Lecturer): self.lecturers.append(lecturer)
    
    def generate_full_report(self):
        print("="*40)
        print("UNIVERSITY FULL REPORT")
        print("="*40)
        for course in self.courses:
            course.display_details()
            print()
        for lecturer in self.lecturers:
            lecturer.print_summary()
            print()
        for student in self.students:
            print(f"Performance for {student.name}:")
            student.show_performance()
            print("-" * 30)