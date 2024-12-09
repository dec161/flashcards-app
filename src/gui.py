import tkinter as tk
from tkinter import ttk, messagebox

from flashcards import IFlashcardSource
from translator import ITranslator


class FlashcardGUI:
    def __init__(self, root, flashcard_source: IFlashcardSource):
        self.__flashcard_source = flashcard_source

        self.__root = root

        ttk.Label(self.__root, text="Угадалка от нас", font=("Arial", 24, "bold"), anchor="center").pack(pady=20)

        self.__word_label = ttk.Label(self.__root, text="", font=("Arial", 30, "bold"), anchor="center")
        self.__word_label.pack(pady=10)

        self.__entry = ttk.Entry(self.__root, font=("Arial", 16), justify="center")
        self.__entry.pack(pady=10)

        self.__show_word_button = ttk.Button(self.__root, text="Показать слово", command=self.__show_word)
        self.__show_word_button.pack(pady=5)

        self.__check_button = ttk.Button(self.__root, text="Проверить перевод", command=self.__check_translation)
        self.__check_button.pack(pady=5)

        self.__message_label = ttk.Label(self.__root, text="", font=("Arial", 16), anchor="center")
        self.__message_label.pack(pady=10)

        self.__stats_label = ttk.Label(self.__root, text="Правильно: 0 | Неправильно: 0", font=("Arial", 14))
        self.__stats_label.pack(pady=10)

    def __update_word_label(self, word):
        self.__word_label.config(text=word)
        self.__entry.delete(0, tk.END)
        self.__message_label.config(text="")

    def __show_word(self):
        self.__flashcard_source.next()
        self.__update_word_label(self.__flashcard_source.current_word)

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

    def __wrong_answer(self):
        self.__message_label.config(
            text=f"Ошибка! Правильный перевод: {self.__flashcard_source.current_translation}",
            foreground="red",
        )
        self.__flashcard_source.wrong_answer()
        self.__update_stats()

    def __update_stats(self):
        """Обновляет статистику."""

        self.__stats_label.config(
            text=f"Правильно: {self.__flashcard_source.total_correct} | Неправильно: {self.__flashcard_source.total_wrong}"
        )


class TranslatorGUI:
    def __init__(self, root, translator: ITranslator):
        self.__root = root
        self.__translator = translator

        ttk.Label(self.__root, text="Переводчик", font=("Arial", 24, "bold"), anchor="center").pack(pady=20)

        ttk.Label(self.__root, text="Введите текст для перевода:", font=("Arial", 14)).pack(pady=10)
        self.input_text = tk.Text(self.__root, font=("Arial", 14), height=5, wrap=tk.WORD)
        self.input_text.pack(pady=5)

        ttk.Label(self.__root, text="Результат перевода:", font=("Arial", 14)).pack(pady=10)
        self.output_text = tk.Text(self.__root, font=("Arial", 14), height=5, wrap=tk.WORD, state=tk.DISABLED)
        self.output_text.pack(pady=5)

        self.translate_button = ttk.Button(self.__root, text="Перевести", command=self.__translate_text)
        self.translate_button.pack(pady=10)

    def __display_text(self, text):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state=tk.DISABLED)

    def __translate_text(self):
        """Перевод текста из текстового поля"""

        input_text = self.input_text.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showerror("Ошибка", "Введите текст для перевода!")
            return

        result = self.__translator.translate(input_text)
        if not result:
            messagebox.showerror("Ошибка", "Не удалось получить перевод")
            return

        self.__display_text(result)
