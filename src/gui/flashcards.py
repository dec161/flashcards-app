import tkinter as tk
from tkinter import ttk, messagebox
from typing import Protocol, Iterable
import matplotlib.pyplot as plt


class IFlashcardSource(Protocol):
    def next(self): pass

    @property
    def current_word(self): pass

    @property
    def current_translation(self): pass

    def correct_answer(self): pass

    def wrong_answer(self): pass

    def save_progress(self): pass

    def reset_answers(self): pass

    def clear_word(self): pass

    @property
    def progress(self) -> Iterable: pass

    @property
    def total_correct(self) -> int: pass

    @property
    def total_wrong(self) -> int: pass


class FlashcardGUI:
    def __init__(self, root, flashcard_source: IFlashcardSource):
        self.__flashcard_source = flashcard_source

        self.__root = root

        ttk.Label(self.__root, text="Угадалка от нас", font=("Arial", 24, "bold"), anchor="center").pack(pady=20)

        self.__word = tk.StringVar()
        self.__word_label = ttk.Label(self.__root, textvariable=self.__word, font=("Arial", 30, "bold"), anchor="center")
        self.__word_label.pack(pady=10)

        self.__entry = ttk.Entry(self.__root, font=("Arial", 16), justify="center")
        self.__entry.pack(pady=10)

        self.__show_word_button = ttk.Button(self.__root, text="Показать слово", command=self.show_word)
        self.__show_word_button.pack(pady=5)

        self.__check_button = ttk.Button(self.__root, text="Проверить перевод", command=self.__check_translation)
        self.__check_button.pack(pady=5)

        self.__message_label = ttk.Label(self.__root, text="", font=("Arial", 16), anchor="center")
        self.__message_label.pack(pady=10)

        self.__stats = tk.StringVar(value="Правильно: 0 | Неправильно: 0")
        self.__stats_label = ttk.Label(self.__root, textvariable=self.__stats, font=("Arial", 14))
        self.__stats_label.pack(pady=10)

        self.__show_progress_button = ttk.Button(self.__root, text="Посмотреть прогресс", command=self.__show_progress)
        self.__show_progress_button.pack()

    def show_word(self):
        self.__flashcard_source.next()
        self.__word.set(self.__flashcard_source.current_word or "")
        self.__entry.delete(0, tk.END)

    def __check_translation(self):
        if not self.__flashcard_source.current_word:
            messagebox.showerror("Ошибка", "Сначала выберите слово!")
            return

        user_input = self.__entry.get().strip().lower()
        if user_input == self.__flashcard_source.current_translation:
            self.__correct_answer()
        else:
            self.__wrong_answer()

    def __correct_answer(self):
        self.__message_label.config(text="Правильно!", foreground="green")
        self.__flashcard_source.correct_answer()
        self.__update_stats()
        self.show_word()

    def __wrong_answer(self):
        self.__message_label.config(
            text=f"Ошибка! Правильный перевод: {self.__flashcard_source.current_translation}",
            foreground="red",
        )
        self.__flashcard_source.wrong_answer()
        self.__update_stats()

    def __update_stats(self):
        """Обновляет статистику."""

        self.__stats.set(f"Правильно: {self.__flashcard_source.total_correct} | Неправильно: {self.__flashcard_source.total_wrong}")

    def clear_word(self):
        self.__flashcard_source.clear_word()
        self.__word.set("")

    def reset_answers(self):
        self.__flashcard_source.reset_answers()
        self.__update_stats()

    def save_progress(self):
        self.__flashcard_source.save_progress()

    def __show_progress(self):
        if not self.__flashcard_source.progress:
            messagebox.showinfo("Прогресс", "Нет данных для отображения")
            return

        correct = [entry["correct"] for entry in self.__flashcard_source.progress]
        wrong = [entry["wrong"] for entry in self.__flashcard_source.progress]

        plt.figure(figsize=(10, 5))
        plt.plot(correct, label="Правильные", color="green", marker="o")
        plt.plot(wrong, label="Неправильные", color="red", marker="x")
        plt.title("Прогресс обучения")
        plt.xlabel("Тесты")
        plt.ylabel("Количество ответов")
        plt.legend()
        plt.grid(True)
        plt.show()
