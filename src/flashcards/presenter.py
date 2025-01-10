import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox

import matplotlib.pyplot as plt

from .protocols import IFlashcardsModel, IFlashcardsView
from src.translator.protocols import ITranslatorPresenter


@dataclass
class FlashcardsPresenter:
    _model: IFlashcardsModel
    _view: IFlashcardsView
    _translator: ITranslatorPresenter

    def show_word(self) -> None:
        self._model.next()
        self._view.set_word(self._model.current_word)
        self._view.focus_entry()

    def check_translation(self) -> None:
        if not self._model.current_word:
            messagebox.showerror("Ошибка", "Сначала выберите слово")
            return

        if self._view.get_answer() != self._model.current_translation:
            self._view.set_message("Неверно!", foreground="red")
            self._model.incorrect_answer()
            self._view.focus_entry()
        else:
            self._view.set_message("Верно!", foreground="green")
            self._model.correct_answer()
            self.show_word()

        self._view.set_stats(
            correct=self._model.total_correct,
            incorrect=self._model.total_incorrect
        )

    def begin_test(self) -> None:
        if not messagebox.askokcancel("Режим теста", "Войти в режим теста?"):
            return

        self._view.set_translator_button_state(tk.DISABLED)
        self._translator.hide()
        self.show_word()
        self._view.show_timer()
        self._view.start_timer()

    def end_test(self) -> None:
        messagebox.showinfo("Режим теста", "Тест завершён!")
        self._view.set_translator_button_state(tk.NORMAL)
        self._model.save_progress()
        self.show_word()
        self._view.hide_timer()

    def show_progress(self) -> None:
        plt.figure(figsize=(10, 5))
        plt.plot(
            self._model.get_correct(),
            label="Правильные",
            color="green",
            marker="o"
        )
        plt.plot(
            self._model.get_incorrect(),
            label="Неправильные",
            color="red",
            marker="x"
        )
        plt.title("Прогресс обучения")
        plt.xlabel("Тесты")
        plt.ylabel("Количество ответов")
        plt.legend()
        plt.grid(True)
        plt.show()

    def show_translator(self) -> None:
        self._translator.show()
