"""
ПРОЕКТ: РЕШАТЕЛЬ УРАВНЕНИЙ НА PYTHON

ВЫБОР ТЕХНОЛОГИЙ:
- Kivy: фреймворк для создания кроссплатформенных мобильных и десктопных приложений
- SymPy: библиотека для символьных математических вычислений

ПОЧЕМУ ИМЕННО ЭТИ ТЕХНОЛОГИИ?
Kivy:
- Бесплатный и с открытым исходным кодом
- Поддержка Windows, macOS, Linux, Android, iOS
- Простота создания GUI без сложных настроек
- Хорошая документация и сообщество

SymPy:
- Точные символьные вычисления (не численные)
- Решение уравнений, упрощение выражений, дифференцирование, интегрирование
- Не требует коммерческой лицензии как MATLAB или Mathematica
- Идеально подходит для образовательных целей
"""

import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

# Преобразования для парсера SymPy - позволяют использовать упрощенный синтаксис
# Например: "2x" вместо "2*x", "x^2" преобразуется в "x**2"
transformations = standard_transformations + (implicit_multiplication_application,)


class EquationSolver(BoxLayout):
    """
    ОСНОВНОЙ КЛАСС ПРИЛОЖЕНИЯ
    Наследуется от BoxLayout - контейнера для организации виджетов вертикально или горизонтально
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Настройка layout Kivy - вертикальное расположение элементов
        self.orientation = "vertical"  # Все виджеты располагаются вертикально
        self.padding = 10  # Отступы от краев окна
        self.spacing = 10  # Расстояние между виджетами

        # ★ БЛОК 1: ВЫБОР ТИПА УРАВНЕНИЯ ★
        # Создаем горизонтальный контейнер для чекбоксов
        self.checkbox_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.15))
        self.checkbox_layout.add_widget(Label(text="Выберите тип уравнения:"))

        # Чекбокс для линейного уравнения
        self.linear_layout = BoxLayout(orientation="horizontal", size_hint=(0.5, 1))
        self.linear_check = CheckBox(group="equation_type", active=True)
        self.linear_check.bind(active=self.on_checkbox_active)
        self.linear_layout.add_widget(self.linear_check)
        self.linear_layout.add_widget(Label(text="Линейное"))
        self.checkbox_layout.add_widget(self.linear_layout)

        # Чекбокс для квадратного уравнения
        self.quadratic_layout = BoxLayout(orientation="horizontal", size_hint=(0.5, 1))
        self.quadratic_check = CheckBox(group="equation_type")
        self.quadratic_check.bind(active=self.on_checkbox_active)
        self.quadratic_layout.add_widget(self.quadratic_check)
        self.quadratic_layout.add_widget(Label(text="Квадратное"))
        self.checkbox_layout.add_widget(self.quadratic_layout)

        self.add_widget(self.checkbox_layout)

        # ★ БЛОК 2: ПОЛЕ ВВОДА ★
        # TextInput - виджет Kivy для ввода текста
        self.equation_input = TextInput(
            hint_text="Введите уравнение (например: 3*x + 2 = 0 или x**2 - 4 = 0)",
            size_hint=(1, 0.2),  # Занимает 100% ширины и 20% высоты
            multiline=False,  # Однострочное поле ввода
        )
        self.add_widget(self.equation_input)

        # ★ БЛОК 3: КНОПКИ УПРАВЛЕНИЯ ★
        # Кнопка решения уравнения
        self.solve_button = Button(text="Решить", size_hint=(1, 0.2))
        self.solve_button.bind(on_press=self.solve)  # Привязка метода к событию нажатия
        self.add_widget(self.solve_button)

        # Кнопка очистки полей
        self.clear_button = Button(text="Очистить", size_hint=(1, 0.2))
        self.clear_button.bind(on_press=self.clear_fields)
        self.add_widget(self.clear_button)

        # ★ БЛОК 4: ПОЛЕ ВЫВОДА РЕЗУЛЬТАТА ★
        self.result_label = Label(
            text="Решение появится здесь",
            size_hint=(1, 0.5),
            halign="left",  # Выравнивание текста по левому краю
            valign="top",  # Выравнивание по верху
        )
        self.result_label.bind(size=self.result_label.setter("text_size"))
        self.add_widget(self.result_label)

    def clear_fields(self, instance):
        """Очищает поле ввода и сбрасывает результат"""
        self.equation_input.text = ""
        self.result_label.text = "Решение появится здесь"

    def on_checkbox_active(self, checkbox, value):
        """
        Обработчик изменения состояния чекбоксов
        Обеспечивает взаимное исключение - только один чекбокс активен
        """
        if value:  # Если чекбокс активируется
            if checkbox == self.linear_check:
                self.quadratic_check.active = False
            else:
                self.linear_check.active = False

    def format_solution(self, solution):
        """
        ФОРМАТИРОВАНИЕ РЕШЕНИЯ ДЛЯ КРАСИВОГО ВЫВОДА
        Использует SymPy для преобразования в числовой формат
        """
        try:
            # sp.N() преобразует символьное выражение в числовое с заданной точностью
            numeric_value = sp.N(solution, n=4)  # n=4 - точность (4 значащие цифры)
            return str(numeric_value)
        except:
            # Если преобразование невозможно, возвращаем исходное решение
            return str(solution)

    def solve(self):
        """
        ОСНОВНОЙ МЕТОД РЕШЕНИЯ УРАВНЕНИЯ
        Объединяет возможности Kivy (GUI) и SymPy (математика)
        """
        try:
            # ★ ЭТАП 1: ОПРЕДЕЛЕНИЕ ТИПА УРАВНЕНИЯ ★
            equation_type = "linear" if self.linear_check.active else "quadratic"
            eq_text = self.equation_input.text.strip()

            # Проверка ввода
            if not eq_text:
                raise ValueError("Введите уравнение")
            if "=" not in eq_text:
                raise ValueError("Уравнение должно содержать знак '='")

            # ★ ЭТАП 2: ПАРСИНГ УРАВНЕНИЯ С ПОМОЩЬЮ SYMPY ★
            lhs_str, rhs_str = eq_text.split("=", 1)

            # parse_expr преобразует строку в математическое выражение SymPy
            lhs = parse_expr(lhs_str, transformations=transformations)
            rhs = parse_expr(rhs_str, transformations=transformations)
            expr = lhs - rhs  # Переносим все в одну сторону: lhs - rhs = 0

            # Создаем символьную переменную x
            x = sp.symbols("x")

            # ★ ЭТАП 3: ПРОВЕРКА СООТВЕТСТВИЯ ТИПУ УРАВНЕНИЯ ★
            degree = sp.degree(expr, x)  # Определяем степень уравнения

            if equation_type == "linear" and degree > 1:
                raise ValueError("Уравнение не линейное (степень > 1)")
            if equation_type == "quadratic" and degree != 2:
                raise ValueError("Уравнение не квадратное (степень должна быть 2)")

            # ★ ЭТАП 4: РЕШЕНИЕ УРАВНЕНИЯ СИМВОЛЬНЫМИ МЕТОДАМИ SYMPY ★
            solutions = sp.solve(expr, x)

            # ★ ЭТАП 5: ФОРМАТИРОВАНИЕ И ВЫВОД РЕЗУЛЬТАТА ★
            if not solutions:
                result_text = "Уравнение не имеет решений"
            else:
                if equation_type == "quadratic":
                    if len(solutions) == 2:
                        x1_formatted = self.format_solution(solutions[0])
                        x2_formatted = self.format_solution(solutions[1])
                        result_text = f"Корни уравнения:\nx1 = {x1_formatted}\nx2 = {x2_formatted}"
                    else:
                        x_formatted = self.format_solution(solutions[0])
                        result_text = f"Корень уравнения (кратный):\nx = {x_formatted}"
                else:
                    x_formatted = self.format_solution(solutions[0])
                    result_text = f"Решение уравнения:\nx = {x_formatted}"

            self.result_label.text = result_text

        except Exception as e:
            # Обработка ошибок с информативным сообщением
            self.result_label.text = f"Ошибка: {str(e)}"


class EquationSolverApp(App):
    """
    ГЛАВНЫЙ КЛАСС ПРИЛОЖЕНИЯ KIVY
    Наследуется от App - базового класса для всех приложений Kivy
    """

    def build(self):
        """Метод build обязателен для Kivy - возвращает корневой виджет"""
        return EquationSolver()


# ТОЧКА ВХОДА ПРИЛОЖЕНИЯ
if __name__ == "__main__":
    """
    ЗАПУСК ПРИЛОЖЕНИЯ:
    - Создается экземпляр EquationSolverApp
    - Вызывается метод run(), который запускает главный цикл Kivy
    - Приложение работает до закрытия окна
    """
    EquationSolverApp().run()
