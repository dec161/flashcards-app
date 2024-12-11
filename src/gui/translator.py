import tkinter as tk
from tkinter import ttk, messagebox

from src.translator import ITranslator


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
