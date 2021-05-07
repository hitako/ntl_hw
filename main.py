class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def get_avg_grade(self):
        mark_sum = 0
        mark_counts = 0
        for course, grades in self.grades.items():
            for grade in grades:
                mark_sum += grade
                mark_counts += 1

        if mark_counts > 0:
            return mark_sum / mark_counts

    def __str__(self):
        return "Имя: " + self.name + "\nФамилия: " + self.surname + "\nСредняя оценка за домашние задания: " \
               + str(self.get_avg_grade()) + "\nКурсы в процессе изучения: " + ', '.join(self.courses_in_progress) \
               + "\nЗавершенные курсы: " + ', '.join(self.finished_courses)

    def __gt__(self, other):
        if not isinstance(other, Lecturer):
            print("Ошибка")
            return
        else:
            return self.get_avg_grade() > other.get_avg_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def has_joint_course(self, student, course):
        return isinstance(student,
                          Student) and course in self.courses_attached and course in student.courses_in_progress


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.student_mark = []

    def set_student_mark(self, student, course, mark):
        if self.has_joint_course(student, course):
            self.student_mark += [mark]
        else:
            return "Ошибка"

    def get_avg_grade(self):
        if len(self.student_mark) > 0:
            mark_sum = 0
            for mark in self.student_mark:
                mark_sum += mark

            return mark_sum / len(self.student_mark)

    def __str__(self):
        return "Имя: " + self.name + "\nФамилия: " + self.surname + "\nСредняя оценка за лекции: " \
               + str(self.get_avg_grade())

    def __gt__(self, other):
        if not isinstance(other, Student):
            print("Ошибка")
            return
        else:
            return self.get_avg_grade() > other.get_avg_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if self.has_joint_course(student, course):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return "Имя: " + self.name + "\nФамилия: " + self.surname


def get_avg_grade_students(students, course):
    if isinstance(students, list):
        grade_sum = 0
        grades_count = 0
        for student in students:
            if not isinstance(student, Student):
                return
            if course in student.grades:
                for grade in student.grades[course]:
                    grade_sum += grade
                    grades_count += 1

        if grades_count > 0:
            return grade_sum / grades_count


male_student = Student('Adam', 'Sandler', 'M')
male_student.courses_in_progress += ['Python', 'Git']

female_student = Student('Kira', 'Nightly', 'F')
female_student.courses_in_progress += ['Java', 'Python', 'PHP']

first_reviewer = Reviewer('Some', 'Buddy')
first_reviewer.courses_attached += ['Python', 'Git']

second_reviewer = Reviewer('David', 'Galustyan')
second_reviewer.courses_attached += ['Java', 'PHP']

first_reviewer.rate_hw(male_student, 'Python', 10)
first_reviewer.rate_hw(male_student, 'Python', 7)
first_reviewer.rate_hw(female_student, 'Python', 10)
first_reviewer.rate_hw(female_student, 'PHP', 9)

second_reviewer.rate_hw(male_student, 'Git', 10)
second_reviewer.rate_hw(male_student, 'Git', 9)
second_reviewer.rate_hw(female_student, 'Java', 10)
second_reviewer.rate_hw(female_student, 'Java', 9)

first_lecturer = Lecturer("First", "Firstov")
first_lecturer.courses_attached += ['Python', 'Git']
first_lecturer.set_student_mark(male_student, 'Python', 5)
first_lecturer.set_student_mark(female_student, 'Python', 7)

second_lecturer = Lecturer("Second", "Secondov")
second_lecturer.courses_attached += ['Java', 'PHP', 'Git']
second_lecturer.set_student_mark(male_student, 'Git', 5)
second_lecturer.set_student_mark(male_student, 'Git', 7)
second_lecturer.set_student_mark(female_student, 'Java', 7)
second_lecturer.set_student_mark(female_student, 'Java', 10)


print(get_avg_grade_students([male_student, female_student], 'Python'))