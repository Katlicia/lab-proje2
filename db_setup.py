from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Department, Course, Classroom, User
import os
from dotenv import load_dotenv

# Göreceli yol kullanarak veritabanı dosyasını mevcut dizinde oluştur
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ders_programi.db')

app = Flask(__name__)
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def setup_database():
    with app.app_context():
        # Veritabanı tablolarını sil ve yeniden oluştur
        print("Veritabanı tabloları siliniyor...")
        db.drop_all()
        print("Veritabanı tabloları yeniden oluşturuluyor...")
        db.create_all()
        
        # Bölümleri ekle
        departments = [
            {'code': 'BLM', 'name': 'Bilgisayar Mühendisliği'},
            {'code': 'YZM', 'name': 'Yazılım Mühendisliği'}
        ]
        
        for dept_data in departments:
            existing_dept = Department.query.filter_by(code=dept_data['code']).first()
            if not existing_dept:
                dept = Department(**dept_data)
                db.session.add(dept)
        
        # Derslikleri ekle
        classrooms = [
            {'code': 'M101', 'capacity': 66, 'type': 'NORMAL'},
            {'code': 'M201', 'capacity': 141, 'type': 'NORMAL'},
            {'code': 'M301', 'capacity': 141, 'type': 'NORMAL'},
            {'code': 'S101', 'capacity': 138, 'type': 'NORMAL'},
            {'code': 'S201', 'capacity': 60, 'type': 'NORMAL'},
            {'code': 'S202', 'capacity': 60, 'type': 'NORMAL'},
            {'code': 'D101', 'capacity': 87, 'type': 'NORMAL'},
            {'code': 'D102', 'capacity': 87, 'type': 'NORMAL'},
            {'code': 'D103', 'capacity': 88, 'type': 'NORMAL'},
            {'code': 'D104', 'capacity': 56, 'type': 'NORMAL'},
            {'code': 'D201', 'capacity': 87, 'type': 'NORMAL'},
            {'code': 'D202', 'capacity': 56, 'type': 'NORMAL'},
            {'code': 'D301', 'capacity': 88, 'type': 'NORMAL'},
            {'code': 'D302', 'capacity': 56, 'type': 'NORMAL'},
            {'code': 'D401', 'capacity': 88, 'type': 'NORMAL'},
            {'code': 'D402', 'capacity': 56, 'type': 'NORMAL'},
            {'code': 'D403', 'capacity': 56, 'type': 'NORMAL'},
            {'code': 'AMFİ A', 'capacity': 143, 'type': 'NORMAL'},
            {'code': 'AMFİ B', 'capacity': 143, 'type': 'NORMAL'},
            {'code': 'BİL.LAB 1', 'capacity': 40, 'type': 'LAB'},
            {'code': 'BİL.LAB.2', 'capacity': 30, 'type': 'LAB'},
            {'code': 'KÜÇÜK LAB', 'capacity': 20, 'type': 'LAB'},
            {'code': 'Online', 'capacity': 999, 'type': 'LAB'}
        ]
        
        for classroom_data in classrooms:
            existing_classroom = Classroom.query.filter_by(code=classroom_data['code']).first()
            if not existing_classroom:
                classroom = Classroom(**classroom_data)
                db.session.add(classroom)
        
        # Dersleri ekle
        courses = [
            # BLM Dersleri
            {'code': 'MAT110', 'name': 'Matematik I', 'theory': 3, 'practice': 2, 'credits': 5, 'semester': 1, 'department_code': 'BLM'},
            {'code': 'FIZ110', 'name': 'Fizik I', 'theory': 3, 'practice': 2, 'credits': 5, 'semester': 1, 'department_code': 'BLM'},
            {'code': 'MAT125', 'name': 'Lineer Cebir', 'theory': 3, 'practice': 0, 'credits': 3, 'semester': 1, 'department_code': 'BLM'},
            {'code': 'BLM111', 'name': 'Bilgisayar Mühendisliğine Giriş', 'theory': 2, 'practice': 0, 'credits': 3, 'semester': 1, 'department_code': 'BLM'},
            {'code': 'BLM112', 'name': 'Bilgisayar Programlama I', 'theory': 3, 'practice': 0, 'credits': 4, 'semester': 1, 'department_code': 'BLM'},
            {'code': 'BLM113', 'name': 'Bilgisayar Lab I', 'theory': 0, 'practice': 2, 'credits': 3, 'semester': 1, 'department_code': 'BLM'},
            {'code': 'DİL101', 'name': 'İngilizce', 'theory': 4, 'practice': 0, 'credits': 4, 'semester': 1, 'department_code': 'BLM'},
            
            {'code': 'MAT120', 'name': 'Matematik II', 'theory': 3, 'practice': 2, 'credits': 5, 'semester': 2, 'department_code': 'BLM'},
            {'code': 'FIZ120', 'name': 'Fizik II', 'theory': 3, 'practice': 2, 'credits': 5, 'semester': 2, 'department_code': 'BLM'},
            {'code': 'ATA102', 'name': 'Atatürk İlkeleri ve İnkılap Tarihi', 'theory': 4, 'practice': 0, 'credits': 4, 'semester': 2, 'department_code': 'BLM'},
            {'code': 'TUR102', 'name': 'Türk Dili', 'theory': 4, 'practice': 0, 'credits': 4, 'semester': 2, 'department_code': 'BLM'},
            {'code': 'BLM121', 'name': 'Bilgisayar Lab II', 'theory': 0, 'practice': 2, 'credits': 3, 'semester': 2, 'department_code': 'BLM'},
            {'code': 'BLM122', 'name': 'Bilgisayar Programlama II', 'theory': 3, 'practice': 0, 'credits': 4, 'semester': 2, 'department_code': 'BLM'},
            {'code': 'BLM123', 'name': 'Elektrik Devre Temelleri', 'theory': 3, 'practice': 0, 'credits': 5, 'semester': 2, 'department_code': 'BLM'},
            
            {'code': 'MAT211', 'name': 'Diferansiyel Denklemler', 'theory': 3, 'practice': 0, 'credits': 4, 'semester': 3, 'department_code': 'BLM'},
            {'code': 'MAT213', 'name': 'Ayrık Matematik', 'theory': 3, 'practice': 0, 'credits': 4, 'semester': 3, 'department_code': 'BLM'},
            {'code': 'BLM211', 'name': 'Nesneye Yönelik Programlama', 'theory': 3, 'practice': 1, 'credits': 5, 'semester': 3, 'department_code': 'BLM'},
            {'code': 'BLM213', 'name': 'Veritabanı Yönetim Sistemleri', 'theory': 3, 'practice': 0, 'credits': 5, 'semester': 3, 'department_code': 'BLM'},
            {'code': 'BLM215', 'name': 'Temel Elektronik ve Uygulamaları', 'theory': 2, 'practice': 1, 'credits': 4, 'semester': 3, 'department_code': 'BLM'},
            {'code': 'BLM217', 'name': 'Programlama Lab-I', 'theory': 0, 'practice': 3, 'credits': 5, 'semester': 3, 'department_code': 'BLM'},
            
            {'code': 'MAT222', 'name': 'Olasılık ve İstatistik', 'theory': 3, 'practice': 0, 'credits': 4, 'semester': 4, 'department_code': 'BLM'},
            {'code': 'BLM2320', 'name': 'Bilgisayar Ağları', 'theory': 3, 'practice': 0, 'credits': 5, 'semester': 4, 'department_code': 'BLM'},
            {'code': 'BLM224', 'name': 'Veri Yapıları', 'theory': 3, 'practice': 1, 'credits': 5, 'semester': 4, 'department_code': 'BLM'},
            {'code': 'BLM226', 'name': 'Sayısal Tasarım ve Uygulamaları', 'theory': 2, 'practice': 1, 'credits': 4, 'semester': 4, 'department_code': 'BLM'},
            {'code': 'YZM228', 'name': 'Programlama Lab-II', 'theory': 0, 'practice': 3, 'credits': 5, 'semester': 4, 'department_code': 'BLM'},
            
            {'code': 'MAT310', 'name': 'Sayısal Yöntemler', 'theory': 3, 'practice': 0, 'credits': 4, 'semester': 5, 'department_code': 'BLM'},
            {'code': 'BLM311', 'name': 'Bilgisayar Mimarisi ve Organizasyonu', 'theory': 3, 'practice': 0, 'credits': 4, 'semester': 5, 'department_code': 'BLM'},
            {'code': 'BLM313', 'name': 'Yazılım Mühendisliği', 'theory': 3, 'practice': 0, 'credits': 5, 'semester': 5, 'department_code': 'BLM'},
            {'code': 'BLM315', 'name': 'Yazılım Lab-I', 'theory': 0, 'practice': 3, 'credits': 5, 'semester': 5, 'department_code': 'BLM'},
            {'code': 'BLM317', 'name': 'Yapay Zeka', 'theory': 3, 'practice': 0, 'credits': 5, 'semester': 5, 'department_code': 'BLM'},
            
            {'code': 'BLM320', 'name': 'Algoritma Tasarımı ve Analizi', 'theory': 3, 'practice': 0, 'credits': 5, 'semester': 6, 'department_code': 'BLM'},
            {'code': 'BLM322', 'name': 'İşletim Sistemleri', 'theory': 3, 'practice': 0, 'credits': 5, 'semester': 6, 'department_code': 'BLM'},
            {'code': 'BLM324', 'name': 'Yazılım Lab-II', 'theory': 0, 'practice': 3, 'credits': 5, 'semester': 6, 'department_code': 'BLM'},
            
            {'code': 'BLM411', 'name': 'Programlama Dilleri', 'theory': 3, 'practice': 0, 'credits': 5, 'semester': 7, 'department_code': 'BLM'},
            {'code': 'BLM413', 'name': 'Biçimsel Diller ve Otomatlar', 'theory': 3, 'practice': 0, 'credits': 5, 'semester': 7, 'department_code': 'BLM'},
            {'code': 'BLM415', 'name': 'Araştırma Problemleri', 'theory': 3, 'practice': 0, 'credits': 4, 'semester': 7, 'department_code': 'BLM'},
            {'code': 'BLM417', 'name': 'İş Sağlığı ve Güvenliği-I', 'theory': 2, 'practice': 0, 'credits': 2, 'semester': 7, 'department_code': 'BLM'},
            
            {'code': 'BLM420', 'name': 'Bilişim Etiği ve Hukuku', 'theory': 3, 'practice': 0, 'credits': 4, 'semester': 8, 'department_code': 'BLM'},
            {'code': 'BLM422', 'name': 'Bitirme Çalışması', 'theory': 0, 'practice': 3, 'credits': 10, 'semester': 8, 'department_code': 'BLM'},
            {'code': 'BLM426', 'name': 'İş Sağlığı ve Güvenliği-II', 'theory': 2, 'practice': 0, 'credits': 2, 'semester': 8, 'department_code': 'BLM'},
            
            # YZM Dersleri
            {'code': 'MAT110', 'name': 'Matematik I', 'theory': 3, 'practice': 2, 'credits': 5, 'semester': 1, 'department_code': 'YZM'},
            {'code': 'FIZ110', 'name': 'Fizik I', 'theory': 3, 'practice': 2, 'credits': 5, 'semester': 1, 'department_code': 'YZM'},
            {'code': 'MAT125', 'name': 'Lineer Cebir', 'theory': 3, 'practice': 0, 'credits': 3, 'semester': 1, 'department_code': 'YZM'},
            {'code': 'YZM111', 'name': 'Yazılım Mühendisliğine Giriş', 'theory': 2, 'practice': 0, 'credits': 3, 'semester': 1, 'department_code': 'YZM'},
            {'code': 'YZM113', 'name': 'Bilgisayar Programlama I', 'theory': 3, 'practice': 0, 'credits': 4, 'semester': 1, 'department_code': 'YZM'},
            {'code': 'YZM115', 'name': 'Bilgisayar Lab I', 'theory': 0, 'practice': 2, 'credits': 3, 'semester': 1, 'department_code': 'YZM'},
            {'code': 'DİL101', 'name': 'İngilizce', 'theory': 4, 'practice': 0, 'credits': 4, 'semester': 1, 'department_code': 'YZM'},
            
            {'code': 'MAT120', 'name': 'Matematik II', 'theory': 3, 'practice': 2, 'credits': 5, 'semester': 2, 'department_code': 'YZM'},
            {'code': 'FIZ120', 'name': 'Fizik II', 'theory': 3, 'practice': 2, 'credits': 5, 'semester': 2, 'department_code': 'YZM'},
            {'code': 'ATA102', 'name': 'Atatürk İlkeleri ve İnkılap Tarihi', 'theory': 4, 'practice': 0, 'credits': 4, 'semester': 2, 'department_code': 'YZM'},
            {'code': 'TUR102', 'name': 'Türk Dili', 'theory': 4, 'practice': 0, 'credits': 4, 'semester': 2, 'department_code': 'YZM'},
            {'code': 'YZM122', 'name': 'Bilgisayar Programlama II', 'theory': 3, 'practice': 0, 'credits': 4, 'semester': 2, 'department_code': 'YZM'},
            {'code': 'YZM124', 'name': 'Bilgisayar Lab II', 'theory': 0, 'practice': 2, 'credits': 3, 'semester': 2, 'department_code': 'YZM'},
            {'code': 'YZM126', 'name': 'Web Teknolojileri', 'theory': 2, 'practice': 1, 'credits': 5, 'semester': 2, 'department_code': 'YZM'},
            
            {'code': 'MAT213', 'name': 'Ayrık Matematik', 'theory': 3, 'practice': 0, 'credits': 4, 'semester': 3, 'department_code': 'YZM'},
            {'code': 'YZM211', 'name': 'Nesneye Yönelik Programlama', 'theory': 3, 'practice': 1, 'credits': 5, 'semester': 3, 'department_code': 'YZM'},
            {'code': 'YZM224', 'name': 'Veritabanı Yönetim Sistemleri', 'theory': 3, 'practice': 0, 'credits': 5, 'semester': 3, 'department_code': 'YZM'},
            {'code': 'YZM215', 'name': 'Yazılım Gereksinim Analizi', 'theory': 2, 'practice': 1, 'credits': 5, 'semester': 3, 'department_code': 'YZM'},
            {'code': 'YZM217', 'name': 'Programlama Lab-I', 'theory': 0, 'practice': 3, 'credits': 5, 'semester': 3, 'department_code': 'YZM'},
            
            {'code': 'YZM317', 'name': 'Bilgisayar Ağları', 'theory': 3, 'practice': 0, 'credits': 5, 'semester': 4, 'department_code': 'YZM'},
            {'code': 'MAT222', 'name': 'Olasılık ve İstatistik', 'theory': 3, 'practice': 0, 'credits': 4, 'semester': 4, 'department_code': 'YZM'},
            {'code': 'YZM213', 'name': 'Veri Yapıları', 'theory': 3, 'practice': 1, 'credits': 5, 'semester': 4, 'department_code': 'YZM'},
            {'code': 'YZM226', 'name': 'Yazılım Tasarımı', 'theory': 2, 'practice': 1, 'credits': 4, 'semester': 4, 'department_code': 'YZM'},
            {'code': 'YZM228', 'name': 'Programlama Lab-II', 'theory': 0, 'practice': 3, 'credits': 5, 'semester': 4, 'department_code': 'YZM'},
            
            {'code': 'YZM313', 'name': 'Yazılım Test ve Kalite', 'theory': 3, 'practice': 0, 'credits': 3, 'semester': 5, 'department_code': 'YZM'},
            {'code': 'YZM315', 'name': 'Yazılım Lab-I', 'theory': 0, 'practice': 3, 'credits': 4, 'semester': 5, 'department_code': 'YZM'},
            {'code': 'MAT220', 'name': 'Sayısal Yöntemler', 'theory': 3, 'practice': 0, 'credits': 4, 'semester': 5, 'department_code': 'YZM'},
            {'code': 'YZM326', 'name': 'Bilgisayar Mimarisi ve Organizasyonu', 'theory': 3, 'practice': 0, 'credits': 4, 'semester': 5, 'department_code': 'YZM'},
            {'code': 'YZM319', 'name': 'Web Programlama', 'theory': 3, 'practice': 0, 'credits': 4, 'semester': 5, 'department_code': 'YZM'},
            {'code': 'BLM424', 'name': 'Yapay Zeka', 'theory': 3, 'practice': 0, 'credits': 4, 'semester': 5, 'department_code': 'YZM'},
            
            {'code': 'YZM322', 'name': 'Algoritma Tasarımı ve Analizi', 'theory': 3, 'practice': 0, 'credits': 4, 'semester': 6, 'department_code': 'YZM'},
            {'code': 'YZM324', 'name': 'Yazılım Lab-II', 'theory': 0, 'practice': 3, 'credits': 4, 'semester': 6, 'department_code': 'YZM'},
            {'code': 'YZM311', 'name': 'İşletim Sistemleri', 'theory': 3, 'practice': 0, 'credits': 5, 'semester': 6, 'department_code': 'YZM'},
            {'code': 'YZM411', 'name': 'Yazılım Proje Yönetimi', 'theory': 3, 'practice': 1, 'credits': 5, 'semester': 6, 'department_code': 'YZM'},
            
            {'code': 'YZM413', 'name': 'Yazılım Mimarisi ve Tasarımı', 'theory': 3, 'practice': 0, 'credits': 5, 'semester': 7, 'department_code': 'YZM'},
            {'code': 'YZM415', 'name': 'Yazılım Doğrulama ve Geçerleme', 'theory': 3, 'practice': 0, 'credits': 4, 'semester': 7, 'department_code': 'YZM'},
            {'code': 'YZM417', 'name': 'İş Sağlığı ve Güvenliği-I', 'theory': 2, 'practice': 0, 'credits': 2, 'semester': 7, 'department_code': 'YZM'},
            {'code': 'YZM419', 'name': 'Araştırma Problemleri', 'theory': 3, 'practice': 0, 'credits': 4, 'semester': 7, 'department_code': 'YZM'},
            
            {'code': 'YZM420', 'name': 'Bilişim Etiği ve Hukuku', 'theory': 3, 'practice': 0, 'credits': 4, 'semester': 8, 'department_code': 'YZM'},
            {'code': 'YZM422', 'name': 'Bitirme Çalışması', 'theory': 0, 'practice': 3, 'credits': 10, 'semester': 8, 'department_code': 'YZM'},
            {'code': 'YZM426', 'name': 'İş Sağlığı ve Güvenliği-II', 'theory': 2, 'practice': 0, 'credits': 2, 'semester': 8, 'department_code': 'YZM'}
        ]
        
        for course_data in courses:
            existing_course = Course.query.filter_by(code=course_data['code']).first()
            if not existing_course:
                # Bölüm kodunu bul
                dept = Department.query.filter_by(code=course_data['department_code']).first()
                if dept:
                    # department_id yerine departments ilişkisini kullanıyoruz
                    # department_code parametresini kaldır
                    dept_code = course_data['department_code']
                    del course_data['department_code']
                    
                    # Yeni alanlar için varsayılan değerleri ekle
                    if 'course_type' not in course_data:
                        course_type = 'yüzyüze'
                        # Ders kodu Online ise otomatik olarak online yap
                        if dept_code == 'Online':
                            course_type = 'online'
                        course_data['course_type'] = course_type
                    
                    if 'capacity' not in course_data:
                        course_data['capacity'] = 30
                    
                    # Ders nesnesini oluştur
                    course = Course(**course_data)
                    
                    # Bölümü departments ilişkisine ekle
                    course.departments.append(dept)
                    
                    db.session.add(course)
                    
        # Ortak dersleri belirle ve ikinci bölüme de ekle
        # MAT, FIZ, DİL, ATA, TUR ile başlayan dersler ortak derslerdir
        common_prefixes = ['MAT', 'FIZ', 'DİL', 'ATA', 'TUR']
        
        # Tüm dersleri çekip, ortak olanları diğer bölüme de ekleyelim
        all_courses = Course.query.all()
        blm_dept = Department.query.filter_by(code='BLM').first()
        yzm_dept = Department.query.filter_by(code='YZM').first()
        
        for course in all_courses:
            # Kod ön eki ortak derslerden biri mi?
            if any(course.code.startswith(prefix) for prefix in common_prefixes):
                # Şu anda hangi bölümlere ait?
                current_dept_ids = [dept.id for dept in course.departments]
                
                # Hem BLM hem YZM'de olması gerekir
                if blm_dept.id not in current_dept_ids and yzm_dept:
                    course.departments.append(blm_dept)
                    
                if yzm_dept.id not in current_dept_ids and blm_dept:
                    course.departments.append(yzm_dept)
        
        # Admin kullanıcısını ekle
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                name='Admin',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        db.session.commit()
        print("Veritabanı başarıyla oluşturuldu!")

if __name__ == '__main__':
    setup_database() 