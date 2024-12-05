import tkinter as tk
from tkinter import ttk, messagebox
import random
import matplotlib.pyplot as plt
from googletrans import Translator


class FlashcardsApp:
    def translate_text(self):
        """Перевод текста из текстового поля."""
        input_text = self.input_text.get("1.0", tk.END).strip()  # Получаем текст из текстового поля
        if not input_text:
            messagebox.showerror("Ошибка", "Введите текст для перевода!")
            return

        try:
            # Определяем направление перевода
            if self.translate_direction == "EN-RU":
                translated_obj = self.translator.translate(input_text, src='en', dest='ru')
            else:
                translated_obj = self.translator.translate(input_text, src='ru', dest='en')

            # Проверка на None
            if not translated_obj or not translated_obj.text:
                raise ValueError("Не удалось получить перевод.")

            # Выводим результат перевода
            translated = translated_obj.text
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, translated)
            self.output_text.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при переводе текста: {e}")

    def __init__(self, root):
        self.root = root
        self.root.title("Угадалка от нас")
        self.root.geometry("1200x600")
        self.root.configure(bg="#2e2e2e")

        self.default_words = {
            "cat": "кот",
            "dog": "собака",
            "apple": "яблоко",
            "car": "машина",
            "house": "дом",
            "sun": "солнце",
            "moon": "луна",
            "tree": "дерево",
            "sky": "небо",
            "water": "вода",
        }
        self.words = self.default_words.copy()
        self.errors = {word: 0 for word in self.words.keys()}
        self.current_word = None
        self.correct_answers = 0
        self.wrong_answers = 0
        self.test_mode = False
        self.time_remaining = 30
        self.timer_id = None
        self.progress = []
        self.translate_direction = "EN-RU"
        self.translator = Translator()

        self.flashcards_frame = tk.Frame(root, bg="#2e2e2e")
        self.flashcards_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.title_label = ttk.Label(
            self.flashcards_frame, text="Угадалка от нас", font=("Arial", 24, "bold"), anchor="center"
        )
        self.title_label.pack(pady=20)

        self.word_label = ttk.Label(self.flashcards_frame, text="", font=("Arial", 30, "bold"), anchor="center")
        self.word_label.pack(pady=10)

        self.entry = ttk.Entry(self.flashcards_frame, font=("Arial", 16), justify="center")
        self.entry.pack(pady=10)

        self.show_word_button = ttk.Button(self.flashcards_frame, text="Показать слово", command=self.show_word)
        self.show_word_button.pack(pady=5)

        self.check_button = ttk.Button(self.flashcards_frame, text="Проверить перевод", command=self.check_translation)
        self.check_button.pack(pady=5)

        self.message_label = ttk.Label(self.flashcards_frame, text="", font=("Arial", 16), anchor="center")
        self.message_label.pack(pady=10)

        self.stats_label = ttk.Label(self.flashcards_frame, text="Правильно: 0 | Неправильно: 0", font=("Arial", 14))
        self.stats_label.pack(pady=10)

        self.test_button = ttk.Button(self.flashcards_frame, text="Режим теста", command=self.start_test)
        self.test_button.pack(pady=10)

        self.timer_label = ttk.Label(self.flashcards_frame, text="", font=("Arial", 16))
        self.timer_label.pack(pady=10)

        self.translator_frame = tk.Frame(root, bg="#2e2e2e")
        self.translator_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(self.translator_frame, text="Переводчик", font=("Arial", 24, "bold"), anchor="center").pack(pady=20)

        ttk.Label(self.translator_frame, text="Введите текст для перевода:", font=("Arial", 14)).pack(pady=10)
        self.input_text = tk.Text(self.translator_frame, font=("Arial", 14), height=5, wrap=tk.WORD)
        self.input_text.pack(pady=5)

        ttk.Label(self.translator_frame, text="Результат перевода:", font=("Arial", 14)).pack(pady=10)
        self.output_text = tk.Text(self.translator_frame, font=("Arial", 14), height=5, wrap=tk.WORD, state=tk.DISABLED)
        self.output_text.pack(pady=5)

        self.translate_button = ttk.Button(self.translator_frame, text="Перевести", command=self.translate_text)
        self.translate_button.pack(pady=10)

    def show_word(self):
        """Показывает новое слово для изучения"""
        if not self.words:
            messagebox.showinfo("Информация", "Нет слов для изучения!")
            return

        # Увеличиваем вероятность слов, на которых были ошибки
        weighted_words = []
        for word, mistakes in self.errors.items():
            weighted_words.extend([word] * (1 + mistakes))

        self.current_word = random.choice(weighted_words)
        self.word_label.config(text=self.current_word)
        self.entry.delete(0, tk.END)
        self.message_label.config(text="")

    def check_translation(self):
        """Проверяет правильность перевода"""
        if not self.current_word:
            messagebox.showerror("Ошибка", "Сначала выберите слово!")
            return

        user_input = self.entry.get().strip().lower()
        if user_input == self.words[self.current_word].lower():
            self.message_label.config(text="Правильно!", foreground="green")
            self.correct_answers += 1
            self.errors[self.current_word] = max(0, self.errors[self.current_word] - 1)  # Уменьшаем ошибки
        else:
            self.message_label.config(
                text=f"Ошибка! Правильный перевод: {self.words[self.current_word]}",
                foreground="red",
            )
            self.wrong_answers += 1
            self.errors[self.current_word] += 1  # Увеличиваем ошибки

        self.update_stats()
        if self.test_mode:
            self.show_word()

    def update_stats(self):
        """Обновляет статистику"""
        self.stats_label.config(
            text=f"Правильно: {self.correct_answers} | Неправильно: {self.wrong_answers}"
        )

    def start_test(self):
        """Запускает режим теста."""
        self.test_mode = True
        self.correct_answers = 0
        self.wrong_answers = 0
        self.time_remaining = 30
        self.update_stats()
        self.show_word()
        self.timer_label.config(text="Осталось времени: 30 сек.")
        self.run_timer()

    def stop_test(self):
        """Останавливает режим теста."""
        self.test_mode = False
        self.word_label.config(text="")
        self.timer_label.config(text="")
        self.message_label.config(text="Тест завершен!")
        self.progress.append({"correct": self.correct_answers, "wrong": self.wrong_answers})
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

    def run_timer(self):
        """Запускает таймер для режима теста."""
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.timer_label.config(text=f"Осталось времени: {self.time_remaining} сек.")
            self.timer_id = self.root.after(1000, self.run_timer)
        else:
            self.stop_test()

    def add_word(self):
        """Добавление нового слова в словарь."""
        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить слово")
        add_window.geometry("300x200")

        tk.Label(add_window, text="Слово (на английском):").pack(pady=10)
        word_entry = tk.Entry(add_window, font=("Arial", 14))
        word_entry.pack(pady=5)

        tk.Label(add_window, text="Перевод:").pack(pady=10)
        translation_entry = tk.Entry(add_window, font=("Arial", 14))
        translation_entry.pack(pady=5)

        def save_word():
            word = word_entry.get().strip()
            translation = translation_entry.get().strip()
            if word and translation:
                self.words[word] = translation
                self.errors[word] = 0
                messagebox.showinfo("Успех", f"Слово '{word}' добавлено в словарь!")
                add_window.destroy()
            else:
                messagebox.showerror("Ошибка", "Заполните оба поля!")

        tk.Button(add_window, text="Сохранить", command=save_word).pack(pady=10)

    def show_progress(self):
        """Показывает прогресс в виде графика."""
        if not self.progress:
            messagebox.showinfo("Прогресс", "Нет данных для отображения.")
            return

        correct = [entry["correct"] for entry in self.progress]
        wrong = [entry["wrong"] for entry in self.progress]

        plt.figure(figsize=(10, 5))
        plt.plot(correct, label="Правильные", color="green", marker="o")
        plt.plot(wrong, label="Неправильные", color="red", marker="x")
        plt.title("Прогресс обучения")
        plt.xlabel("Тесты")
        plt.ylabel("Количество ответов")
        plt.legend()
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardsApp(root)
    root.mainloop()
