from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Ders-Bölüm ilişki tablosu (many-to-many)
course_department = db.Table('course_department',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('department_id', db.Integer, db.ForeignKey('departments.id'), primary_key=True)
)

# Öğrenci-Ders ilişki tablosu (many-to-many)
student_course = db.Table('student_course',
    db.Column('student_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('semester', db.Integer, nullable=False),  # Hangi dönemde alındığı
    db.Column('grade', db.Float),  # Ders notu (varsa)
    db.Column('status', db.String(20), default='active')  # active, passed, failed
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, instructor, student
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    
    # Yeni eklenen alanlar
    is_active = db.Column(db.Boolean, default=True)
    max_weekly_hours = db.Column(db.Integer, default=20)  # Haftalık maksimum ders saati
    current_semester = db.Column(db.Integer, default=1)  # Öğrencinin mevcut yarıyılı
    student_number = db.Column(db.String(20), unique=True)  # Öğrenci numarası
    
    # İlişkiler
    department = db.relationship('Department', backref='users')
    courses = db.relationship('Course', backref='instructor', lazy=True)
    unavailable_times = db.relationship('UnavailableTime', backref='instructor', lazy=True)
    selected_courses = db.relationship('Course', secondary=student_course, 
                                     backref=db.backref('students', lazy='dynamic'))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    # İlişki kısmını kaldırdık çünkü çoka-çok ilişki kurduk


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    theory = db.Column(db.Integer, nullable=False)  # Teori ders saati
    practice = db.Column(db.Integer, nullable=False)  # Uygulama ders saati
    credits = db.Column(db.Integer, nullable=False)  # Kredi
    semester = db.Column(db.Integer, nullable=False)  # Yarıyıl
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Yeni alanlar
    course_type = db.Column(db.String(20), default='yüzyüze')  # 'online' veya 'yüzyüze'
    capacity = db.Column(db.Integer, default=30)  # Dersin kontenjanı
    
    # department_id alanını kaldırıp, çoka-çok ilişki ekliyoruz
    departments = db.relationship('Department', secondary=course_department, 
                                 backref=db.backref('courses', lazy='dynamic'))
    
    # Yeni eklenen alanlar
    is_mandatory = db.Column(db.Boolean, default=True)  # Zorunlu/Seçmeli ders
    preferred_days = db.Column(db.String(100))  # Tercih edilen günler (örn: "Pazartesi,Salı")
    preferred_times = db.Column(db.String(100))  # Tercih edilen saatler (örn: "09:00-12:00")
    min_students = db.Column(db.Integer, default=0)  # Minimum öğrenci sayısı (seçmeli dersler için)
    
    # İlişkiler
    schedule_items = db.relationship('Schedule', backref='course', lazy=True)


class Classroom(db.Model):
    __tablename__ = 'classrooms'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # NORMAL, LAB
    schedule_items = db.relationship('Schedule', backref='classroom', lazy=True)


class Schedule(db.Model):
    __tablename__ = 'schedule_items'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'), nullable=False)
    day = db.Column(db.String(20), nullable=False)  # Pazartesi, Salı, ...
    start_time = db.Column(db.String(5), nullable=False)  # HH:MM formatında
    end_time = db.Column(db.String(5), nullable=False)  # HH:MM formatında


# Yeni eklenen model: Öğretim üyelerinin müsait olmadığı zamanlar
class UnavailableTime(db.Model):
    __tablename__ = 'unavailable_times'

    id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    day = db.Column(db.String(20), nullable=False)  # Pazartesi, Salı, ...
    start_time = db.Column(db.String(5), nullable=False)  # HH:MM formatında
    end_time = db.Column(db.String(5), nullable=False)  # HH:MM formatında
    reason = db.Column(db.String(200))  # Müsait olmama nedeni (opsiyonel)