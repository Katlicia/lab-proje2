from flask import Flask
import os
from models import db, Department, Course, Classroom, User, Schedule
from dotenv import load_dotenv

# Göreceli yolları kullanarak dizinleri belirle
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ders_programi.db')

# Flask uygulamasını oluştur ve yapılandır
app = Flask(__name__)

# Veritabanı bağlantısı için .env dosyasından bilgileri oku
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Veritabanını başlat
db.init_app(app)

def add_common_courses():
    with app.app_context():
        blm_dept = Department.query.filter_by(code='BLM').first()
        yzm_dept = Department.query.filter_by(code='YZM').first()
        
        if not blm_dept or not yzm_dept:
            print("BLM veya YZM bölümü bulunamadı!")
            return
            
        # Eklenmesi gereken ortak dersler (resimlerden belirlendi)
        # YZM için daha benzersiz kodlar kullanacağız
        common_courses = [
            # BLM Kodu, YZM Kodu, İsim ve diğer bilgiler
            {'blm_code': 'MAT110', 'yzm_code': 'MAT110Y', 'name': 'Matematik I', 'semester': 1, 'T': 3, 'P': 2, 'C': 5},
            {'blm_code': 'FIZ110', 'yzm_code': 'FIZ110Y', 'name': 'Fizik I', 'semester': 1, 'T': 3, 'P': 2, 'C': 5},
            {'blm_code': 'MAT125', 'yzm_code': 'MAT125Y', 'name': 'Lineer Cebir', 'semester': 1, 'T': 3, 'P': 0, 'C': 4},
            {'blm_code': 'DİL101', 'yzm_code': 'DİL101Y', 'name': 'İngilizce', 'semester': 1, 'T': 4, 'P': 0, 'C': 4},
            
            # 2. Yarıyıl
            {'blm_code': 'MAT120', 'yzm_code': 'MAT120Y', 'name': 'Matematik II', 'semester': 2, 'T': 3, 'P': 2, 'C': 5},
            {'blm_code': 'FIZ120', 'yzm_code': 'FIZ120Y', 'name': 'Fizik II', 'semester': 2, 'T': 3, 'P': 2, 'C': 5},
            {'blm_code': 'ATA102', 'yzm_code': 'ATA102Y', 'name': 'Atatürk İlkeleri ve İnkılap Tarihi', 'semester': 2, 'T': 4, 'P': 0, 'C': 4},
            {'blm_code': 'TUR102', 'yzm_code': 'TUR102Y', 'name': 'Türk Dili', 'semester': 2, 'T': 4, 'P': 0, 'C': 4},
            
            # 3. Yarıyıl
            {'blm_code': 'MAT213', 'yzm_code': 'MAT213Y', 'name': 'Ayrık Matematik', 'semester': 3, 'T': 3, 'P': 0, 'C': 4},
            
            # 4. Yarıyıl
            {'blm_code': 'MAT222', 'yzm_code': 'MAT222Y', 'name': 'Olasılık ve İstatistik', 'semester': 4, 'T': 3, 'P': 0, 'C': 4},
            
            # 5. Yarıyıl (Güz)
            {'blm_code': 'MAT310', 'yzm_code': 'MAT310Y', 'name': 'Sayısal Yöntemler', 'semester': 5, 'T': 3, 'P': 0, 'C': 4},
        ]
        
        # Eklenen dersler için liste
        added_courses = []
        
        # Her ders için kontrol et ve gerekiyorsa ekle
        for course_data in common_courses:
            # Bu dersin BLM versiyonu var mı?
            blm_course = Course.query.filter_by(
                code=course_data['blm_code'], 
                department_id=blm_dept.id
            ).first()
            
            if not blm_course:
                print(f"UYARI: {course_data['blm_code']} dersi BLM bölümünde bulunamadı, eklenemiyor.")
                continue
                
            # Bu dersin YZM versiyonu zaten var mı?
            yzm_course = Course.query.filter_by(
                code=course_data['yzm_code'], 
                department_id=yzm_dept.id
            ).first()
            
            # YZM'de yoksa ekle
            if not yzm_course:
                instructor_id = blm_course.instructor_id
                
                # Yeni YZM dersi ekle
                new_course = Course(
                    code=course_data['yzm_code'],
                    name=course_data['name'],
                    department_id=yzm_dept.id,
                    instructor_id=instructor_id,
                    semester=course_data['semester'],
                    theory=course_data['T'],
                    practice=course_data['P'],
                    credits=course_data['C'],
                    is_mandatory=True  # Temel dersler zorunlu olacak
                )
                
                db.session.add(new_course)
                added_courses.append({
                    'blm_code': course_data['blm_code'],
                    'yzm_code': course_data['yzm_code'],
                    'name': course_data['name'],
                    'semester': course_data['semester']
                })
                
        if added_courses:
            db.session.commit()
            print("Aşağıdaki dersler YZM bölümüne eklendi:")
            for course in added_courses:
                print(f"- {course['name']} (BLM: {course['blm_code']}, YZM: {course['yzm_code']}, Yarıyıl: {course['semester']})")
                
            print("\nAlgoritma için ortak dersleri belirtin:")
            for course in added_courses:
                print(f"Ortak Ders: {course['blm_code']} ve {course['yzm_code']} - {course['name']}")
        else:
            print("Eklenecek ders bulunamadı.")
            
        # Şimdi veritabanını temizle (ortak derse çevirelim)
        db.session.commit()

if __name__ == "__main__":
    add_common_courses() 