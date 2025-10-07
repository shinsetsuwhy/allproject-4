import pytest
import os
import tempfile
from app import read_students_from_md, find_student, generate_greeting

class TestStudentData:
    """Тесты для работы с данными студентов"""
    
    def test_read_students_with_new_metrics(self):
        """Тест чтения студентов с новыми метриками"""
        students = read_students_from_md('students.md')
        
        assert len(students) > 0
        student = students[0]
        
        # Проверяем наличие всех новых полей
        assert 'full_name' in student
        assert 'group' in student
        assert 'college' in student
        assert 'admission_year' in student
        assert 'course' in student
        
        # Проверяем типы данных
        assert isinstance(student['full_name'], str)
        assert isinstance(student['group'], str)
        assert isinstance(student['college'], str)
        assert isinstance(student['admission_year'], int)
        assert isinstance(student['course'], int)
    
    def test_find_student_by_full_name(self):
        """Тест поиска студента по ФИО"""
        test_students = [
            {
                'full_name': 'Иванов Иван Иванович',
                'group': 'ТВ-101',
                'college': 'Технический колледж',
                'admission_year': 2023,
                'course': 2
            }
        ]
        
        student = find_student(test_students, 'Иванов Иван Иванович')
        assert student is not None
        assert student['group'] == 'ТВ-101'
        assert student['college'] == 'Технический колледж'
    
    def test_student_metrics_validation(self):
        """Тест валидности метрик студентов"""
        students = read_students_from_md('students.md')
        
        for student in students:
            # Проверяем корректность года поступления
            assert 2000 <= student['admission_year'] <= 2024
            # Проверяем корректность курса
            assert 1 <= student['course'] <= 6
            # Проверяем, что все поля заполнены
            assert student['full_name'] != ''
            assert student['group'] != ''
            assert student['college'] != ''

class TestGreetingLogic:
    """Тесты для логики приветствия и регистрации"""
    
    def test_generate_greeting_contains_all_metrics(self):
        """Тест, что приветствие содержит все метрики"""
        test_student = {
            'full_name': 'Тестовый Студент',
            'group': 'ТЕСТ-101',
            'college': 'Тестовый колледж',
            'admission_year': 2023,
            'course': 2
        }
        
        greeting = generate_greeting(test_student)
        
        # Проверяем наличие всех метрик в приветствии
        assert test_student['full_name'] in greeting
        assert test_student['group'] in greeting
        assert test_student['college'] in greeting
        assert str(test_student['admission_year']) in greeting
        assert str(test_student['course']) in greeting
        
        # Проверяем дополнительные вычисляемые метрики
        assert 'Лет обучения' in greeting
    
    def test_greeting_course_specific_messages(self):
        """Тест специальных сообщений для разных курсов"""
        # Тест для первого курса
        first_year_student = {
            'full_name': 'Студент 1 курс',
            'group': 'ГР-101',
            'college': 'Колледж',
            'admission_year': 2024,
            'course': 1
        }
        
        greeting_1 = generate_greeting(first_year_student)
        assert 'начинаете' in greeting_1.lower()
        
        # Тест для старших курсов
        senior_student = {
            'full_name': 'Студент 3 курс',
            'group': 'ГР-301',
            'college': 'Колледж',
            'admission_year': 2022,
            'course': 3
        }
        
        greeting_3 = generate_greeting(senior_student)
        assert 'опытный' in greeting_3.lower() or 'диплом' in greeting_3.lower()
    
    def test_student_years_calculation(self):
        """Тест расчета лет обучения"""
        test_student = {
            'full_name': 'Тестовый Студент',
            'group': 'ТЕСТ-101',
            'college': 'Тестовый колледж',
            'admission_year': 2022,
            'course': 3
        }
        
        greeting = generate_greeting(test_student)
        # Должно быть 3 года обучения (2024-2022+1)
        assert '3' in greeting

class TestIntegration:
    """Интеграционные тесты всего приложения"""
    
    def test_complete_student_workflow(self):
        """Тест полного workflow приложения"""
        # Чтение данных
        students = read_students_from_md('students.md')
        assert len(students) > 0
        
        # Поиск существующего студента
        if students:
            existing_student = find_student(students, students[0]['full_name'])
            assert existing_student is not None
            
            # Генерация приветствия
            greeting = generate_greeting(existing_student)
            assert existing_student['full_name'] in greeting
    
    def test_data_consistency(self):
        """Тест согласованности данных"""
        students = read_students_from_md('students.md')
        
        for student in students:
            # Проверяем, что курс соответствует году поступления
            expected_min_course = 2024 - student['admission_year'] + 1
            # Допускаем погрешность в 1 курс
            assert abs(student['course'] - expected_min_course) <= 1
    
    def test_file_modification_integration(self):
        """Тест интеграции с файловой системой"""
        # Создаем временный файл для тестирования
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("""# Test Students
| ФИО | Группа | Колледж | Год поступления | Курс |
|-----|--------|---------|-----------------|------|
| Тест Студент | Т-001 | Тест колледж | 2023 | 2 |""")
            temp_filename = f.name
        
        try:
            students = read_students_from_md(temp_filename)
            assert len(students) == 1
            assert students[0]['full_name'] == 'Тест Студент'
        finally:
            os.unlink(temp_filename)