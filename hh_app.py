from flask import Flask, render_template, request, url_for, redirect
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy.orm import declarative_base
import os
from sqlalchemy import create_engine
from sqlalchemy import func
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

db_user = "sqlmaster"
db_password = "VOf67bY6kR"
db_host = "92.63.177.19"
db_name = "hh_ithub_msod"
schema_name = "jobsearch"

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# --- Database Models ---
class Vacancy(Base):
    __tablename__ = 'vacancies'
    __table_args__ = {'schema': schema_name}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    employer = Column(String)
    salary_from = Column(String)
    experience = Column(String)
    description = Column(String)
    published_at = Column(DateTime)

    vacancy_skills = relationship("VacancySkill", back_populates="vacancy")


class UniqueSkill(Base):
    __tablename__ = 'skills'
    __table_args__ = {'schema': schema_name}

    id = Column(Integer, primary_key=True, autoincrement=True)
    skill = Column(String(255), nullable=False, unique=True)

    vacancy_skills = relationship("VacancySkill", back_populates="skill")
    student_skills = relationship("StudentSkill", back_populates="skill")

class VacancySkill(Base):
    __tablename__ = 'vacancy_skills'
    __table_args__ = {'schema': schema_name}

    id = Column(Integer, primary_key=True, autoincrement=True)
    vacancy_id = Column(Integer, ForeignKey(f'{schema_name}.vacancies.id'), nullable=False)
    skill_id = Column(Integer, ForeignKey(f'{schema_name}.skills.id'), nullable=False)

    vacancy = relationship("Vacancy", back_populates="vacancy_skills")
    skill = relationship("UniqueSkill", back_populates="vacancy_skills")

class Students(Base):
    __tablename__ = 'students'
    __table_args__ = {'schema': schema_name}

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)

    student_skills = relationship("StudentSkill", back_populates="student")


class StudentSkill(Base):
    __tablename__ = 'student_skills'
    __table_args__ = {'schema': schema_name}

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey(f'{schema_name}.students.id'), nullable=False)
    skill_id = Column(Integer, ForeignKey(f'{schema_name}.skills.id'), nullable=False)

    student = relationship("Students", back_populates="student_skills")
    skill = relationship("UniqueSkill", back_populates="student_skills")

# --- Flask Application ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Замените на надежный секретный ключ
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


skills_dictionary = {
    "Data Engineer": [
        "Python", "SQL", "Apache Airflow", "ETL", "DWH", "Big Data", "Kafka", "Greenplum",
        "PostgreSQL", "Linux", "AWS", "Google Cloud Platform", "Google Big Query",
        "Yandex Data Lens", "DBT", "Debezium", "Access", "S3", "AirByte", "ByteBase", "Flink",
        "Redash", "Ceph", "RedPanda", "Teradata", "ORACLE", "Apache Kafka", "Hadoop",
        "Spark", "sklearn", "Data Mining", "Data Science", "Математический анализ", "Аналитические исследования",
        "Data Analysis", "DWH", "Big Data", "OLAP", "ELT", "Superset", "Grafana",
        "Elasticsearch", "Теория вероятности", "Исследовательский анализ данных", "Решение проблем",
        "Kafka", "Greenplum", "ETL-процессы", "PyTorch", "TensorFlow", "tree-based algorithms",
        "Bash", "Airflow", "Redis", "Jupyter", "Clickhouse", "SQLAlchemy ORM", "MongoDB",
        "RabbitMQ", "Gitlab", "S3", "OLAP",  "Информационные технологии",  "Highload",
        "DataLens", "Google BigQuery", "Cloud Data", "Интернет-маркетинг", "NoSQL"
    ],

    "Java Разработчик": [
        "Java", "Java Core", "Сollections Framework", "Multithreading", "REST API", "HATEOAS",
        "PostgreSQL", "SOLID", "KISS", "DRY", "YAGNI", "GoF", "CI/CD", "k8s", "Docker",
        "Алгоритмы и структуры данных", "Spring Framework", "Maven", "Spring Boot", "RESTful",
        "SOAP API", "Backend", "Microservices", "Layered pattern", "DDD", "CQRS & EventSourcing",
        "Java Script", "React.js", "Cypress", "TestCafe", "Gradle", "Java SE", "Java Servlets",
        "HTTP", "Debian", "Ubuntu", "RHEL", "Spring Data", "Spring Web", "Hibernate ORM",
        "JUnit", "Jira", "Apache Maven", "Liquibase", "Kotlin", "Hibernate",
        "Автоматизированное тестирование", "SoapUI", "Mockito", "Prometheus", "Рефакторинг кода",
        "Микросервисная архитектура", "Код-ревью", "Spring Core", "Spring", "Web API", "Spring Data",
        "Spring Web", "JEE", "Spring", "Maven", "Tomcat", "Jetty", "jOOQ", "gRPC",
        "Consul", "OAuth", "OAUTH", "Spring Cloud", "Hibernate", "JDBC", "Spring Boot",
        "Thymeleaf", "Swagger", "Netty", "Microservices", "Redis", "Kafka", "IBM MQ", "RabbitMQ, etc",
        "MVC", "WCF", "EF.Core", "EF core", "Dapper", "Orleans", "ADO.NET", "gRPC",
        "CDI", "JPA", "Servlet", "JSP", "JSF"

    ],

    "Разработчик игр": [
        "gamedev", "Системный анализ", "C#", "Computer Vision", "OpenVINO", "cv::dnn", "Gamedev",
        "C#", "3D Моделирование", "High poly", "Low poly", "Графика", "Разработка компьютерных Игр",
        "3D", "3D Max", "3D-графика", "3ds Max", "Текстурирование", "Crash Bandicoot", "Gambling",
        "Анимация", "Game Programming", "Narrative design", "Написание сценариев", "GameDev",
        "Blender 3D", "Unity", "UI", "Figma", "Three.js", "Creativity", " Соблюдение дедлайнов",
        "Умение работать в условиях многозадачности", "C++", "3D", "VR", "Game Engine", "PS5", "Системный гейм-дизайн",
        "ГДД", "MVP", "Разработка игровых механик", "Blueprints", ".NET Framework", "mobile", "Godot", "GDScript",
        "Game Development", "Unreal Engine", "AI", "Unity 3D", "Анимация",
        "Three.js", "Креативность", "Соблюдение дедлайнов", "Умение работать в условиях многозадачности", "Game Programming",
        "MongoDB", "Нарративный дизайн", "Системный подход", "Middle", "Написание сценариев", "Написание текстов", "Agile",
        "GDD", "Внутренняя документация", "UX", "Unreal Engine", "GitHub", "Perforce", "AI", "Unity 3D", "Анимация",
        "Three.js", "Креативность", " Соблюдение дедлайнов", "Умение работать в условиях многозадачности", "Game Programming",
        "MongoDB", "Нарративный дизайн", "Системный подход", "Middle", "Написание сценариев", "Написание текстов", "Atlassian Confluence",
        "C", "Xbox", "PlayStation", "GDD, ","AI, ", "Lua","Unity 3d, PS5, Canvas, pixijs, ", "3D Modelirovanie,"
        "3D Max, 3D-grafika, Gambling,Three.js, Three Js, Системный гейм-дизайн "

    ],

    "Маркетинг": [
        "Медиапланирование", "Продвижение бренда", "Маркетинговые коммуникации", "Маркетинговые исследования",
        "B2C маркетинг", "Маркетинговый анализ", "Маркетинговая стратегия", "Трейд-маркетинговая стратегия",
        "Инфлюенс-маркетинг", "Маркетинговые метрики", "Позиционирование бренда", "Интернет-маркетинг",
        "Контент-маркетинг", "Разработка контент-плана", "Масштабирование маркетинговых кампаний",
        "Анализ эффективности маркетинговых кампаний", "Маркетинговый аудит", "Медиа-мониторинг",
        "Целевой маркетинг", "Контентная стратегия", "Развитие бренда", "Планирование рекламных кампаний",
        "1С-Битрикс", "SMM", "Яндекс.Директ", "Сквозная аналитика", "Roistat", "B2B-маркетинг", "Брендинг",
        "Дизайн рассылок", "Ведение групп в социальных сетях", "Дизайн презентаций",
        "Анализ целевой аудитории", "Локальные маркетинговые кампании", "Email-маркетинг", "Оптимизация воронки продаж",
        "Анализ конкурентной среды", "Привлечение новых клиентов", "Оптимизация логистических процессов", "Управление репутацией",
        "Анализ рынка", "Вывод продукта на рынок", "Управление ассортиментом", "CorelDRAW", "Rich-контент", "Digital Marketing",
        "amoCRM", "Customer Support", "Контекстная реклама", "Первичная бухгалтерская документация", "E-mail рассылки", "Нейромаркетинг",
        "Управленческая отчетность", "Умение работать в коллективе", "Медиапланирование", "Медиа-мониторинг", "международные маркетинговые кампании",
        "Маркетинговые коммуникации","маркетинговый анализ", "маркетинговая стратегия", "контент маркетинг, ""B2C Marketing"
    ],

    "Реклама": [
        "Запуск контекстных кампаний", "Реклама", "Продюсер", "Adobe Premier Pro", "Рекламная съемка",
        "Интернет-реклама", "Создание креативов", "Публикация контента", "Посты для социальных сетей",
        "Запуск федеральных рекламных кампаний", "Интернет маркетинг", "Типографика",
        "Adobe After Effects", "Дизайн наружной реклама", "Внутренняя реклама", "Подбор контента",
        "Ретаргетинг", "Навыки работы с возражениями", "Интернет маркетинг", "анализ эффективности маркетинговых кампаний",
         "таргетированная реклама","медийная реклама", "проведение промо акций"
    ],

    ".NET разработчик": [
        ".NET Framework", "C#", ".NET", "ASP.NET", "ASP.NET Core", "ASP.NET MVC", "Entity Framework",
        "LINQ", "SQL Server", "MVC", ".NET Core", "Microsoft Visual Studio", "WPF", "XML", "Visual Studio C#",
        "NHibernate", "Active Directory", "PowerShell", "Win32 Api", "Terrasoft CRM", "MSSQL",
        "Creatio", ".NET 8", "Clean Architecture", "TFS", "Signal R", "Xamarin", "MAUI", "Dapr",
        "Dapper", "ADO.NET", ".Net", "REST", "gRPC", "Microservices", "Docker", "Kubernetes",
        "C#", "gRPC, DDD", ".NET Core, EF Core, EF core, blazor,", " ASP .Net, Web API,",
        "Swagger, Cqrs, SOA"

    ],

}

# --- Helper Functions ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def get_vacancies_with_skills(db, skill_categories=None):
    """
    Получает вакансии из базы данных и фильтрует их на основе указанных категорий навыков.

    Args:
        db: Сессия базы данных.
        skill_categories: Список категорий навыков для фильтрации (необязательный).

    Returns:
        Список словарей, представляющих вакансии.
    """

    vacancies = db.query(Vacancy)

    if skill_categories:
        # Собираем все навыки из выбранных категорий
        skills_to_filter = []
        for category in skill_categories:
            skills_to_filter.extend(skills_dictionary.get(category, []))
        skills_to_filter_lower = [skill.lower() for skill in skills_to_filter]

        if skills_to_filter:
            vacancies = vacancies.join(VacancySkill).join(UniqueSkill).filter(func.lower(UniqueSkill.skill).in_(skills_to_filter_lower))
            print(vacancies.statement.compile(compile_kwargs={"literal_binds": True}))

    vacancies = vacancies.all()
    vacancies_data = []
    for vacancy in vacancies:
        skills = [skill.skill.skill for skill in vacancy.vacancy_skills]
        vacancies_data.append({
            'id': vacancy.id,
            'name': vacancy.name,
            'employer': vacancy.employer,
            'salary_from': vacancy.salary_from,
            'experience': vacancy.experience,
            'description': vacancy.description,
            'published_at': vacancy.published_at,
            'skills': skills
        })
    return vacancies_data

# Функция для подсчета совпадений навыков и добавления весов
def count_skill_matches(vacancy, student_skills):
    vacancy_skills = [skill.skill.skill for skill in vacancy.vacancy_skills]
    matches = set(student_skills).intersection(vacancy_skills)
    if not matches:
        return 0  # Нет совпадений - возвращаем 0

    # Добавим веса для разных навыков (пример)
    weights = {
        "Python": 2,
        "SQL": 1.5,
        "Java": 1.8  # Добавьте другие навыки и веса по необходимости
    }

    weighted_score = sum(weights.get(match, 1) for match in matches)
    return weighted_score

# --- Routes ---
@app.route("/")
def index():
    db = next(get_db())
    skill_categories = request.args.getlist('skill_categories')
    vacancies = get_vacancies_with_skills(db, skill_categories=skill_categories)
    students = db.query(Students).all()  # Получаем всех студентов
    return render_template("index.html", vacancies=vacancies, all_skills=skills_dictionary, selected_categories=skill_categories, students=students)

@app.route("/vacancy/<int:vacancy_id>")
def vacancy_detail(vacancy_id):
    db = next(get_db())
    vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()

    if vacancy is None:
        return "Vacancy not found", 404

    skills = [skill.skill.skill for skill in vacancy.vacancy_skills]

    vacancy_data = {
        'id': vacancy.id,
        'name': vacancy.name,
        'employer': vacancy.employer,
        'salary_from': vacancy.salary_from,
        'experience': vacancy.experience,
        'description': vacancy.description,
        'published_at': vacancy.published_at,
        'skills': skills
    }
    return render_template("vacancy_detail.html", vacancy=vacancy_data)


@app.route("/salary_dashboard")
def salary_dashboard():
    db = next(get_db())

    # Запрашиваем среднюю зарплату по направлению
    salary_data = (
        db.query(VacancySkill.skill_id, func.avg(Vacancy.salary_from))
        .join(Vacancy)
        .group_by(VacancySkill.skill_id)
        .all()
    )

    skills_with_salary = []
    for skill_id, avg_salary in salary_data:
        skill = db.query(UniqueSkill).filter(UniqueSkill.id == skill_id).first()
        if skill:
            skills_with_salary.append({'skill': skill.skill, 'avg_salary': avg_salary})

    return render_template("salary_dashboard.html", skills_with_salary=skills_with_salary)






@app.route("/vacancy_count_dashboard")
def vacancy_count_dashboard():
    db = next(get_db())

    # Запрашиваем количество вакансий по направлению
    vacancy_count_data = (
        db.query(VacancySkill.skill_id, func.count(Vacancy.id))
        .join(Vacancy)
        .group_by(VacancySkill.skill_id)
        .all()
    )

    skills_with_vacancy_count = []
    for skill_id, vacancy_count in vacancy_count_data:
        skill = db.query(UniqueSkill).filter(UniqueSkill.id == skill_id).first()
        if skill:
            skills_with_vacancy_count.append({'skill': skill.skill, 'vacancy_count': vacancy_count})

    return render_template("vacancy_count_dashboard.html", skills_with_vacancy_count=skills_with_vacancy_count)



















@app.route("/add_student", methods=['GET', 'POST'])
def add_student():
    db = next(get_db())
    form = AddStudentForm()
    students = db.query(Students).all()  # Получаем всех студентов
    # Заполняем список навыков в форме
    form.skills.choices = [(skill.id, skill.skill) for skill in db.query(UniqueSkill).all()]

    if form.validate_on_submit():
        # Создаем нового студента
        new_student = Students(full_name=form.full_name.data)
        db.add(new_student)
        db.commit()
        db.refresh(new_student)  # Получаем ID нового студента

        # Связываем выбранные навыки со студентом
        selected_skill_ids = form.skills.data
        for skill_id in selected_skill_ids:
            skill = db.query(UniqueSkill).get(skill_id) # Получаем навык по ID
            if skill:
                student_skill = StudentSkill(student_id=new_student.id, skill_id=skill.id)
                db.add(student_skill)

        db.commit()
        return redirect(url_for('index'))  # Перенаправляем на главную страницу

    return render_template("add_student.html", form=form, students=students)

@app.route("/recommendations")
def recommendations():
    db = next(get_db())
    student_id = request.args.get('student_id', type=int)

    if not student_id:
        return "Student ID is required", 400

    student = db.query(Students).filter(Students.id == student_id).first()

    if not student:
        return "Student not found", 404

    student_skills = [skill.skill.skill for skill in student.student_skills]

    vacancies = db.query(Vacancy).all()

    # Используем улучшенную функцию count_skill_matches
    def vacancy_score(vacancy):
        return count_skill_matches(vacancy, student_skills)

    # Фильтруем и сортируем вакансии
    recommended_vacancies = sorted(
        (vacancy for vacancy in vacancies if vacancy_score(vacancy) > 0),  # Фильтруем без совпадений
        key=vacancy_score,
        reverse=True
    )

    recommendations_data = []
    for vacancy in recommended_vacancies:
        skills = [skill.skill.skill for skill in vacancy.vacancy_skills]
        recommendations_data.append({
            'id': vacancy.id,
            'name': vacancy.name,
            'employer': vacancy.employer,
            'salary_from': vacancy.salary_from,
            'experience': vacancy.experience,
            'description': vacancy.description,
            'published_at': vacancy.published_at,
            'skills': skills,
            'skill_matches': vacancy_score(vacancy)  # Используем взвешенную оценку
        })

    return render_template("recommendations.html", student=student, recommendations=recommendations_data)

class AddStudentForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    skills = SelectMultipleField('Skills', coerce=int) # coerce=int преобразует ID навыка в Integer
    submit = SubmitField('Add Student')

# --- Run the Application ---
if __name__ == '__main__':
    app.run(debug=True)