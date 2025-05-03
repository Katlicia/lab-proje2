from flask import Flask
from models import db, Department, Course, Classroom, User, Schedule
import os

# Göreceli yol kullanarak veritabanı dosyasını belirle
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ders_programi.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    print("Bölümler:")
    departments = Department.query.all()
    for dept in departments:
        print(f"- {dept.code}: {dept.name}")
    
    print("\nDerslikler:")
    classrooms = Classroom.query.all()
    print(f"Toplam {len(classrooms)} derslik var")
    for classroom in classrooms:
        print(f"- {classroom.code} (Kapasite: {classroom.capacity}, Tip: {classroom.type})")
    
    print("\nDersler:")
    courses = Course.query.all()
    print(f"Toplam {len(courses)} ders var")
    print("\nBLM Bölümü Dersleri:")
    blm_dept = Department.query.filter_by(code='BLM').first()
    if blm_dept:
        blm_courses = Course.query.filter_by(department_id=blm_dept.id).all()
        for course in blm_courses:
            print(f"- {course.code}: {course.name} (T:{course.theory} P:{course.practice} K:{course.credits})")
    
    print("\nYZM Bölümü Dersleri:")
    yzm_dept = Department.query.filter_by(code='YZM').first()
    if yzm_dept:
        yzm_courses = Course.query.filter_by(department_id=yzm_dept.id).all()
        for course in yzm_courses:
            print(f"- {course.code}: {course.name} (T:{course.theory} P:{course.practice} K:{course.credits})")
    
    print("\nKullanıcılar:")
    users = User.query.all()
    print(f"Toplam {len(users)} kullanıcı var")
    for user in users:
        print(f"- {user.username} ({user.name}, {user.role})")
    
    print("\nDers Programı:")
    schedules = Schedule.query.all()
    print(f"Toplam {len(schedules)} ders programı kaydı var")
    for schedule in schedules:
        course = Course.query.get(schedule.course_id)
        classroom = Classroom.query.get(schedule.classroom_id)
        if course and classroom:
            print(f"- {course.code} ({classroom.code}): {schedule.day} {schedule.start_time}-{schedule.end_time}") 