from typing import List
from college import Student, Course
import utils

def calculate_gpa(student: Student, courses: List[Course]) -> float:
    '''
    This function takes a student and a list of course
    It should compute the GPA for the student
    The GPA is the sum(hours of course * grade in course) / sum(hours of course)
    The grades come in the form: 'A+', 'A' and so on.
    But you can convert the grades to points using a static method in the course class
    To know how to use the Student and Course classes, see the file "college.py"  
    '''
    #TODO: ADD YOUR CODE HERE
    gpa = 0
    total_hours = 0
    for course in courses:
        if student.id in course.grades:
            gpa += course.hours * Course.convert_grade_to_points(course.grades.get(student.id,0))
            total_hours += course.hours
    if total_hours == 0:
        return 0
    return gpa / total_hours
