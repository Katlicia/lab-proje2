from flask import Flask
import os
from models import db, Department, Course, Classroom, User, Schedule
from dotenv import load_dotenv

# Göreceli yolları kullanarak dizinleri belirle
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ders_programi.db')

# Flask uygulamasını oluştur ve yapılandır
app = Flask(__name__)

# Veritabanı kredilerini .env dosyasından yükle
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Veritabanını başlat
db.init_app(app)

def check_common_courses():
    with app.app_context():
        print("\n=== BÖLÜMLER ===")
        departments = Department.query.all()
        for dept in departments:
            print(f"ID: {dept.id}, Kod: {dept.code}, İsim: {dept.name}")
        
        blm_dept = Department.query.filter_by(code='BLM').first()
        yzm_dept = Department.query.filter_by(code='YZM').first()
        
        if not blm_dept or not yzm_dept:
            print("BLM veya YZM bölümü bulunamadı!")
            return
        
        print(f"\n=== MAT/FIZ/İngilizce DERSLERİ ===")
        mat_fiz_courses = Course.query.filter(
            (Course.code.like('MAT%') | 
             Course.code.like('FIZ%') |
             Course.code.like('ATA%') |
             Course.code.like('TUR%') |
             Course.code.like('DİL%') |
             Course.code.like('DIL%'))
        ).all()
        
        print("Tüm MAT/FIZ/ATA/TUR/DIL dersleri:")
        for course in mat_fiz_courses:
            dept = Department.query.get(course.department_id)
            dept_code = dept.code if dept else "N/A"
            print(f"ID: {course.id}, Kod: {course.code}, İsim: {course.name}, Bölüm: {dept_code}, Yarıyıl: {course.semester}")
        
        # BLM'de olup YZM'de olmayan ortak dersler
        blm_course_codes = {course.code for course in Course.query.filter_by(department_id=blm_dept.id).all()}
        yzm_course_codes = {course.code for course in Course.query.filter_by(department_id=yzm_dept.id).all()}
        
        print("\n=== BLM'DE OLUP YZM'DE OLMAYAN DERSLER ===")
        for code in sorted(blm_course_codes - yzm_course_codes):
            if code.startswith(('MAT', 'FIZ', 'ATA', 'TUR', 'DIL', 'DİL')):
                course = Course.query.filter_by(code=code).first()
                print(f"Kod: {code}, İsim: {course.name if course else 'Bulunamadı'}, Yarıyıl: {course.semester if course else 'N/A'}")
        
        # Eksik dersleri YZM için ekleme önerisi
        print("\n=== DÜZELTİLMESİ GEREKEN DERSLER ===")
        for code in sorted(blm_course_codes - yzm_course_codes):
            if code.startswith(('MAT', 'FIZ', 'ATA', 'TUR', 'DIL', 'DİL')):
                blm_course = Course.query.filter_by(code=code, department_id=blm_dept.id).first()
                if blm_course:
                    print(f"YZM bölümüne eklenecek: {code} - {blm_course.name} (Yarıyıl: {blm_course.semester})")

if __name__ == "__main__":
    check_common_courses() 