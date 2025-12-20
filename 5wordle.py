import tkinter as tk
from tkinter import messagebox, font
import random


class FwordsGame:
    def __init__(self):
        """Инициализация игры с русскими словами"""

        # РУССКИЙ словарь из 5 букв
        with open("слова.txt", 'r', encoding='utf-8') as f:
            # Каждая строка = отдельное слово
            self.word_list = [line.strip().upper() for line in f if line.strip()]
            # Фильтруем только 5-буквенные слова
            self.word_list = [word for word in self.word_list if len(word) == 5]

        # Выбираем случайное слово
        self.secret_word = random.choice(self.word_list).upper()
        print(f"DEBUG: Загаданное слово: {self.secret_word}")  # Для отладки

        self.max_attempts = 6
        self.current_attempt = 0
        self.current_letter = 0
        self.game_over = False
        self.won = False

        # Русские буквы для клавиатуры
        self.russian_letters = "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"

        # Создаем основное окно
        self.root = tk.Tk()
        self.root.title("5 БУКВ")
        self.root.configure(bg='#121212')
        self.root.resizable(False, False)

        # Центрируем окно
        window_width = 800
        window_height = 1000
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2 - 40
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Создаем шрифты
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.letter_font = font.Font(family="Helvetica", size=22, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=12)
        self.keyboard_font = font.Font(family="Helvetica", size=14, weight="bold")

        # Словарь для отслеживания состояния букв на клавиатуре
        self.keyboard_colors = {}
        for letter in self.russian_letters:
            self.keyboard_colors[letter] = '#818384'  # Серый по умолчанию

        # Инициализируем интерфейс
        self.setup_ui()

        # Биндим клавиши
        self.root.bind('<Key>', self.on_key_press)
        self.root.bind('<Return>', self.submit_guess)
        self.root.bind('<BackSpace>', self.delete_letter)

        # Запускаем главный цикл
        self.root.mainloop()

    def setup_ui(self):
        """Настраивает пользовательский интерфейс"""
        # Заголовок
        title_frame = tk.Frame(self.root, bg='#121212')
        title_frame.pack(pady=20)

        tk.Label(
            title_frame,
            text="5 БУКВ",
            font=self.title_font,
            fg='#6aaa64',
            bg='#121212'
        ).pack()

        # Игровое поле
        self.game_frame = tk.Frame(self.root, bg='#121212')
        self.game_frame.pack(pady=20)

        # Создаем сетку 6x5 для букв
        self.letter_labels = []
        for row in range(self.max_attempts):
            row_labels = []
            for col in range(5):
                label = tk.Label(
                    self.game_frame,
                    text="",
                    width=4,
                    height=2,
                    font=self.letter_font,
                    bg='#121212',
                    fg='#ffffff',
                    relief='raised',
                    borderwidth=2
                )
                label.grid(row=row, column=col, padx=5, pady=5)
                row_labels.append(label)
            self.letter_labels.append(row_labels)

        # РУССКАЯ клавиатура
        self.setup_russian_keyboard()

        # Кнопки управления
        self.setup_control_buttons()

        # Подсказки
        hint_frame = tk.Frame(self.root, bg='#121212')
        hint_frame.pack(pady=10)

        tk.Label(
            hint_frame,
            text="Подсказки:",
            font=("Helvetica", 10),
            fg='#aaaaaa',
            bg='#121212'
        ).pack(side=tk.LEFT, padx=5)

        tk.Label(
            hint_frame,
            text="Зеленый = правильная буква на месте",
            font=("Helvetica", 10),
            fg='#6aaa64',
            bg='#121212'
        ).pack(side=tk.LEFT, padx=5)

        tk.Label(
            hint_frame,
            text="Желтый = буква есть в слове",
            font=("Helvetica", 10),
            fg='#c9b458',
            bg='#121212'
        ).pack(side=tk.LEFT, padx=5)

        tk.Label(
            hint_frame,
            text="Серый = буквы нет в слове",
            font=("Helvetica", 10),
            fg='#787c7e',
            bg='#121212'
        ).pack(side=tk.LEFT, padx=5)

    def setup_russian_keyboard(self):
        """Создает виртуальную клавиатуру"""
        keyboard_frame = tk.Frame(self.root, bg='#121212')
        keyboard_frame.pack(pady=20)

        # Первый ряд: ЙЦУКЕНГШЩЗХЪ
        row1_frame = tk.Frame(keyboard_frame, bg='#121212')
        row1_frame.pack(pady=3)
        row1 = "ЙЦУКЕНГШЩЗХЪ"
        self.keyboard_buttons_row1 = []
        for letter in row1:
            btn = tk.Button(
                row1_frame,
                text=letter,
                width=3,
                height=2,
                font=self.keyboard_font,
                bg='#818384',
                fg='#ffffff',
                command=lambda l=letter: self.on_keyboard_click(l),
                relief='raised',
                borderwidth=2
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            self.keyboard_buttons_row1.append(btn)

        # Второй ряд: ФЫВАПРОЛДЖЭ
        row2_frame = tk.Frame(keyboard_frame, bg='#121212')
        row2_frame.pack(pady=3)
        row2 = "ФЫВАПРОЛДЖЭ"
        self.keyboard_buttons_row2 = []
        for letter in row2:
            btn = tk.Button(
                row2_frame,
                text=letter,
                width=3,
                height=2,
                font=self.keyboard_font,
                bg='#818384',
                fg='#ffffff',
                command=lambda l=letter: self.on_keyboard_click(l),
                relief='raised',
                borderwidth=2
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            self.keyboard_buttons_row2.append(btn)

        # Третий ряд: ЯЧСМИТЬБЮ + спец. кнопки
        row3_frame = tk.Frame(keyboard_frame, bg='#121212')
        row3_frame.pack(pady=3)

        # Кнопка Enter
        enter_btn = tk.Button(
            row3_frame,
            text="ENTER",
            width=7,
            height=2,
            font=self.keyboard_font,
            bg='#6aaa64',
            fg='#ffffff',
            command=self.submit_guess,
            relief='raised',
            borderwidth=2
        )
        enter_btn.pack(side=tk.LEFT, padx=2, pady=2)

        row3 = "ЯЧСМИТЬБЮ"
        self.keyboard_buttons_row3 = []
        for letter in row3:
            btn = tk.Button(
                row3_frame,
                text=letter,
                width=3,
                height=2,
                font=self.keyboard_font,
                bg='#818384',
                fg='#ffffff',
                command=lambda l=letter: self.on_keyboard_click(l),
                relief='raised',
                borderwidth=2
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            self.keyboard_buttons_row3.append(btn)

        # Кнопка Backspace
        backspace_btn = tk.Button(
            row3_frame,
            text="⌫",
            width=7,
            height=2,
            font=self.keyboard_font,
            bg='#818384',
            fg='#ffffff',
            command=self.delete_letter,
            relief='raised',
            borderwidth=2
        )
        backspace_btn.pack(side=tk.LEFT, padx=2, pady=2)

    def setup_control_buttons(self):
        """Создает кнопки управления и отображение попыток"""
        control_frame = tk.Frame(self.root, bg='#121212')
        control_frame.pack(pady=10)

        # Кнопка "Новая игра" (слева)
        new_game_btn = tk.Button(
            control_frame,
            text="🔄 Новая игра",
            font=self.button_font,
            bg='#6aaa64',
            fg='#ffffff',
            command=self.new_game,
            width=15,
            height=2
        )
        new_game_btn.pack(side=tk.LEFT, padx=5)

        # Надпись с номером попытки (посередине)
        self.status_label = tk.Label(
            control_frame,
            text=f"Попытка: {self.current_attempt + 1}/{self.max_attempts}",
            font=self.button_font,
            bg='#3a3a3c',
            fg='#ffffff',
            width=15,
            height=2,
            relief='raised'
        )
        self.status_label.pack(side=tk.LEFT, padx=5)

        # Кнопка "Правила" (справа)
        rules_btn = tk.Button(
            control_frame,
            text="❓ Правила",
            font=self.button_font,
            bg='#787c7e',
            fg='#ffffff',
            command=self.show_rules,
            width=15,
            height=2
        )
        rules_btn.pack(side=tk.LEFT, padx=5)

    def on_key_press(self, event):
        """Обрабатывает нажатия клавиш """
        if self.game_over:
            return

        key = event.char.upper()
        russian_letters = self.russian_letters

        # Проверяем, что это русская буква
        if key in russian_letters and self.current_letter < 5:
            self.add_letter(key)
        elif event.keysym == 'Return':
            self.submit_guess()
        elif event.keysym == 'BackSpace':
            self.delete_letter()

    def on_keyboard_click(self, letter):
        """Обрабатывает клики по виртуальной клавиатуре"""
        if self.game_over:
            return

        if letter in self.russian_letters and self.current_letter < 5:
            self.add_letter(letter)

    def add_letter(self, letter):
        """Добавляет букву в текущую попытку"""
        if self.current_letter < 5:
            # Обновляем метку в сетке
            label = self.letter_labels[self.current_attempt][self.current_letter]
            label.config(text=letter, bg='#3a3a3c', fg='#ffffff')
            self.current_letter += 1

    def delete_letter(self, event=None):
        """Удаляет последнюю букву"""
        if self.current_letter > 0 and not self.game_over:
            self.current_letter -= 1

            # Очищаем метку в сетке
            label = self.letter_labels[self.current_attempt][self.current_letter]
            label.config(text="", bg='#121212')

    def submit_guess(self, event=None):
        """Отправляет текущую догадку на проверку"""
        if self.game_over:
            return

        # Собираем текущее слово
        guess = ""
        for i in range(5):
            label_text = self.letter_labels[self.current_attempt][i].cget("text")
            if label_text:
                guess += label_text
            else:
                guess += " "

        guess = guess.strip()

        # Проверяем, что слово заполнено
        if len(guess) != 5:
            messagebox.showwarning("Неполное слово", "Введите все 5 букв!")
            return

        # Проверяем слово
        self.check_guess(guess)

    def check_guess(self, guess):
        """Проверяет догадку и обновляет интерфейс"""
        secret_list = list(self.secret_word)
        guess_list = list(guess)
        colors = ['#787c7e'] * 5  # Серый по умолчанию

        # Первый проход: отмечаем правильные буквы (зеленые)
        for i in range(5):
            if guess_list[i] == secret_list[i]:
                colors[i] = '#6aaa64'  # Зеленый
                secret_list[i] = None
                guess_list[i] = None
                self.keyboard_colors[guess[i]] = '#6aaa64'

        # Второй проход: отмечаем буквы на неправильных местах (желтые)
        for i in range(5):
            if guess_list[i] is not None and guess_list[i] in secret_list:
                colors[i] = '#c9b458'  # Желтый
                secret_list[secret_list.index(guess_list[i])] = None
                if self.keyboard_colors[guess[i]] != '#6aaa64':
                    self.keyboard_colors[guess[i]] = '#c9b458'
            elif guess_list[i] is not None:
                if self.keyboard_colors[guess[i]] not in ['#6aaa64', '#c9b458']:
                    self.keyboard_colors[guess[i]] = '#787c7e'

        # Обновляем цвет букв в сетке
        for i in range(5):
            label = self.letter_labels[self.current_attempt][i]
            label.config(bg=colors[i], fg='#ffffff')

        # Обновляем клавиатуру
        self.update_keyboard_colors()

        # Проверяем победу
        if guess == self.secret_word:
            self.won = True
            self.game_over = True
            self.show_result(win=True)
            return

        # Переходим к следующей попытке
        self.current_attempt += 1

        # Проверяем окончание игры
        if self.current_attempt >= self.max_attempts:
            self.game_over = True
            self.show_result(win=False)
            return

        # Сбрасываем текущую букву для новой попытки
        self.current_letter = 0

        # Обновляем статус
        self.status_label.config(
            text=f"Попытка: {self.current_attempt + 1}/{self.max_attempts}"
        )

    def update_keyboard_colors(self):
        """Обновляет цвета клавиш на виртуальной клавиатуре"""
        # Обновляем первый ряд
        for i, letter in enumerate("ЙЦУКЕНГШЩЗХЪ"):
            if letter in self.keyboard_colors:
                btn = self.keyboard_buttons_row1[i]
                color = self.keyboard_colors.get(letter, '#818384')
                btn.config(bg=color)

        # Обновляем второй ряд
        for i, letter in enumerate("ФЫВАПРОЛДЖЭ"):
            if letter in self.keyboard_colors:
                btn = self.keyboard_buttons_row2[i]
                color = self.keyboard_colors.get(letter, '#818384')
                btn.config(bg=color)

        # Обновляем третий ряд
        for i, letter in enumerate("ЯЧСМИТЬБЮЁ"):
            if letter in self.keyboard_colors:
                btn = self.keyboard_buttons_row3[i]
                color = self.keyboard_colors.get(letter, '#818384')
                btn.config(bg=color)

    def show_result(self, win):
        """Показывает результат игры"""
        if win:
            messagebox.showinfo(
                "ПОБЕДА! 🏆 ",
                f"Вы угадали слово '{self.secret_word}' за {self.current_attempt} попыток!"
            )
        else:
            messagebox.showinfo(
                "Увы, конец игры 😔",
                f"Вы не смогли угадать слово.\nЗагаданное слово было: {self.secret_word}"
            )

    def give_hint(self):
        """Дает подсказку игроку"""
        if self.game_over:
            messagebox.showinfo("Игра окончена", "Начните новую игру!")
            return

    def show_rules(self):
        """Показывает правила игры"""
        rules_text = """
        ПРАВИЛА ИГРЫ 5 БУКВ:

        1. Цель игры: угадать скрытое слово из 5 букв
        2. У вас есть 6 попыток
        3. После каждой попытки вы получаете подсказки:
           • 🟩 Зеленый - буква на правильном месте
           • 🟨 Желтый - буква есть в слове, но в другом месте
           • ⬜️ Серый - буквы нет в слове

        4. Используйте подсказки, чтобы сузить варианты
        5. Нажимайте ENTER для отправки слова
        6. Используйте BACKSPACE для удаления букв
        7. Можно вводить буквы с клавиатуры или кликать мышкой
        8. Буква "Ё" учитывается как "Е"

        Удачи! 🎉
        """
        messagebox.showinfo("Правила игры", rules_text)

    def new_game(self):
        """Начинает новую игру"""
        # Сбрасываем состояние игры
        self.secret_word = random.choice(self.word_list).upper()
        print(f"DEBUG: Новое слово: {self.secret_word}")  # Для отладки
        self.current_attempt = 0
        self.current_letter = 0
        self.game_over = False
        self.won = False

        # Очищаем игровое поле
        for row in range(self.max_attempts):
            for col in range(5):
                label = self.letter_labels[row][col]
                label.config(text="", bg='#121212', fg='#ffffff')

        # Сбрасываем цвета клавиатуры
        for letter in self.russian_letters:
            self.keyboard_colors[letter] = '#818384'
        self.update_keyboard_colors()

        # Обновляем статус
        self.status_label.config(
            text=f"Попытка: {self.current_attempt + 1}/{self.max_attempts}"
        )




# Запуск игры
if __name__ == "__main__":
    game = FwordsGame()