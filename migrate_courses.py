from flask import Flask
import os
from models import db, Department, Course, Classroom, User, Schedule, course_department
from sqlalchemy import text, inspect
from dotenv import load_dotenv

# Göreceli yolları kullanarak dizinleri belirle
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ders_programi.db')

# Flask uygulamasını oluştur ve yapılandır
app = Flask(__name__)

# Veritabanı bağlantı bilgilerini .env dosyasından yükle
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Veritabanını başlat
db.init_app(app)

def migrate_courses():
    with app.app_context():
        # Tablo varlığını kontrol et ve yoksa oluştur
        inspector = inspect(db.engine)
        if 'course_department' not in inspector.get_table_names():
            print("course_department tablosu oluşturuluyor...")
            db.create_all()
        
        # Mevcut derslerin department_id değerlerini kontrol et
        courses = Course.query.all()
        
        # Departman ID'leri kullanılır mı kontrol et
        has_department_id = False
        for column in inspector.get_columns('courses'):
            if column['name'] == 'department_id':
                has_department_id = True
                break
        
        if has_department_id:
            print("Mevcut dersleri yeni çoklu bölüm yapısına taşıyorum...")
            # Her ders için çoklu bölüm ilişkisi kur
            for course in courses:
                # Eski department_id'yi al
                old_department_id = None
                try:
                    old_department_id = course.department_id
                except AttributeError:
                    # Eğer department_id alanı yoksa (zaten kaldırılmışsa) geç
                    continue
                
                if old_department_id:
                    # Bölümü bul
                    department = Department.query.get(old_department_id)
                    if department:
                        # Bu bölümü dersin ilişkili bölümlerine ekle
                        if department not in course.departments:
                            course.departments.append(department)
            
            # Değişiklikleri kaydet
            db.session.commit()
            
            # department_id sütununu sil (artık ihtiyaç yok)
            try:
                print("department_id sütunu kaldırılıyor...")
                with db.engine.begin() as conn:
                    conn.execute(text("ALTER TABLE courses DROP COLUMN department_id"))
                print("department_id sütunu başarıyla kaldırıldı.")
            except Exception as e:
                print(f"department_id sütunu kaldırılırken hata: {str(e)}")
        else:
            print("department_id sütunu zaten kaldırılmış.")
        
        # Sonuçları göster
        print("\nBölüm başına ders sayıları:")
        departments = Department.query.all()
        for dept in departments:
            course_count = len(list(dept.courses))
            print(f"{dept.code} ({dept.name}): {course_count} ders")
        
        # Ortak dersleri göster
        print("\nBirden fazla bölüme ait dersler:")
        for course in courses:
            if len(course.departments) > 1:
                dept_codes = ', '.join([d.code for d in course.departments])
                print(f"{course.code} - {course.name}: {dept_codes}")
        
        print("\nMigrasyon tamamlandı!")

if __name__ == "__main__":
    migrate_courses() 