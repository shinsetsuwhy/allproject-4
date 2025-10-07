import re

def read_students_from_md(filename):
    """Читаем данные студентов из markdown файла"""
    students = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Пропускаем заголовки и находим строки таблицы
        for line in lines:
            if '|' in line and line.strip() and 'ФИО' not in line and '---' not in line:
                parts = [part.strip() for part in line.split('|') if part.strip()]
                if len(parts) >= 5:
                    students.append({
                        'full_name': parts[0],
                        'group': parts[1],
                        'college': parts[2],
                        'admission_year': int(parts[3]),
                        'course': int(parts[4])
                    })
                    
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден")
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        
    return students

def find_student(students, full_name):
    """Ищем студента по ФИО"""
    for student in students:
        if student['full_name'].lower() == full_name.lower():
            return student
    return None

def generate_greeting(student):
    """Создаем приветствие с метриками"""
    current_year = 2024
    years_studying = current_year - student['admission_year'] + 1
    
    greeting = f"\n🎓 Добро пожаловать, {student['full_name']}!"
    greeting += f"\n{'='*50}"
    greeting += f"\n📊 Ваши образовательные метрики:"
    greeting += f"\n├─ 🏫 Колледж: {student['college']}"
    greeting += f"\n├─ 👥 Группа: {student['group']}"
    greeting += f"\n├─ 📅 Год поступления: {student['admission_year']}"
    greeting += f"\n├─ 📚 Текущий курс: {student['course']}"
    greeting += f"\n└─ ⏱️ Лет обучения: {years_studying}"
    
    if student['course'] == 1:
        greeting += f"\n\n🌟 Вы только начинаете свой образовательный путь!"
    elif student['course'] >= 3:
        greeting += f"\n\n🎯 Вы уже опытный студент! Скоро диплом!"
    
    return greeting

def display_student_info(student):
    """Показываем информацию о студенте"""
    greeting = generate_greeting(student)
    print(greeting)

def register_new_student(full_name, students, filename):
    """Регистрируем нового студента"""
    print(f"\n❌ Студент {full_name} не найден в базе.")
    response = input("Хотите зарегистрироваться? (да/нет): ").lower().strip()
    
    if response == 'да':
        try:
            print("\n📝 Регистрация нового студента:")
            group = input("Введите учебную группу: ")
            college = input("Введите название колледжа: ")
            admission_year = int(input("Введите год поступления: "))
            course = int(input("Введите текущий курс: "))
            
            # Проверяем данные
            if admission_year < 2000 or admission_year > 2024:
                print("❌ Ошибка: Некорректный год поступления")
                return None
            if course < 1 or course > 6:
                print("❌ Ошибка: Некорректный номер курса")
                return None
            
            new_student = {
                'full_name': full_name,
                'group': group,
                'college': college,
                'admission_year': admission_year,
                'course': course
            }
            students.append(new_student)
            
            # Добавляем в файл
            with open(filename, 'a', encoding='utf-8') as file:
                file.write(f"\n| {full_name} | {group} | {college} | {admission_year} | {course} |")
            
            print("✅ Студент успешно зарегистрирован!")
            return new_student
            
        except ValueError:
            print("❌ Ошибка: Введите корректные числовые значения")
    
    return None

def main():
    """Главная функция программы
    Разработчик: Татаринов Вячеслав Сергеевич
    """
    filename = 'students.md'
    students = read_students_from_md('students.md')
    
    print("🎓 Система управления студентами")
    print("=" * 50)
    print("Разработчик: Татаринов Вячеслав Сергеевич")
    print("Доступные команды:")
    print("• Введите ФИО студента для поиска")
    print("• 'список' - показать всех студентов")
    print("• 'выход' - завершить программу")
    
    while True:
        print("\n" + "-" * 30)
        user_input = input("Введите команду: ").strip()
        
        if user_input.lower() == 'выход':
            print("👋 До свидания!")
            break
        elif user_input.lower() == 'список':
            print("\n📋 Список всех студентов:")
            for i, student in enumerate(students, 1):
                print(f"{i}. {student['full_name']} - {student['group']}")
        else:
            student = find_student(students, user_input)
            
            if student:
                display_student_info(student)
            else:
                new_student = register_new_student(user_input, students, filename)
                if new_student:
                    display_student_info(new_student)

if __name__ == "__main__":
    main()