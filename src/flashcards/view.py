import tkinter as tk
from tkinter import ttk
from typing import Callable

from .protocols import IFlashcardsPresenter


class Timer(ttk.Label):
    def __init__(self,
                 limit: int,
                 on_end: Callable[[], None] | None = None,
                 *args, **kwargs):
        self._limit = limit
        self._score = 0
        self.on_end = on_end

        super().__init__(*args, **kwargs)

        self.config(text=self._score)

    def start(self) -> None:
        self._score = self._limit
        self.config(text=self._score)
        self.after(1000, self._tick)  # noqa

    def _tick(self) -> None:
        self._score -= 1
        self.config(text=self._score)

        if self._score > 0:
            self.after(1000, self._tick)  # noqa
            return

        self.on_end()


class FlashcardsView(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._title_label = ttk.Label(self, text="Угадалка от нас", font=("Arial", 24, "bold"), anchor="center")
        self._title_label.pack(pady=20, expand=True)

        self._word_label = ttk.Label(self, text="test", font=("Arial", 30, "bold"), anchor="center")
        self._word_label.pack(pady=10, expand=True)

        self._timer = Timer(30, font=("Arial", 16), master=self)

        self._entry = ttk.Entry(self, font=("Arial", 16), justify="center")
        self._entry.pack(pady=5, expand=True)

        self._show_word_button = ttk.Button(self, text="Показать слово")
        self._show_word_button.pack(pady=5, expand=True)

        self._check_button = ttk.Button(self, text="Проверить перевод")
        self._check_button.pack(pady=5, expand=True)

        self._message_label = ttk.Label(self, text="", font=("Arial", 16), anchor="center")
        self._message_label.pack(pady=10, expand=True)

        self._stats_label = ttk.Label(self, font=("Arial", 14))
        self._stats_label.pack(pady=10, expand=True)

        self._start_test_button = ttk.Button(self, text="Режим теста")
        self._start_test_button.pack(pady=10, expand=True)

        self._show_progress_button = ttk.Button(self, text="Посмотреть прогресс")
        self._show_progress_button.pack(pady=5, expand=True)

        self._show_translator_button = ttk.Button(self, text="Открыть переводчик")
        self._show_translator_button.pack(expand=True)

        self.config(bg="#2e2e2e")

    def bind_presenter(self, flashcards_presenter: IFlashcardsPresenter) -> None:
        self._timer.on_end = flashcards_presenter.end_test
        self._show_word_button.config(command=flashcards_presenter.show_word)
        self._check_button.config(command=flashcards_presenter.check_translation)
        self._start_test_button.config(command=flashcards_presenter.begin_test)
        self._show_progress_button.config(command=flashcards_presenter.show_progress)
        self._show_translator_button.config(command=flashcards_presenter.show_translator)

    def focus_entry(self) -> None:
        self._entry.focus()

    def show_timer(self) -> None:
        self._timer.pack(after=self._check_button)

    def hide_timer(self) -> None:
        self._timer.pack_forget()

    def get_answer(self) -> str:
        return self._entry.get().strip().lower()

    def set_word(self, word: str) -> None:
        self._word_label.config(text=word)
        self._entry.delete(0, tk.END)

    def set_message(self, text: str, *, foreground: str) -> None:
        self._message_label.config(text=text, foreground=foreground)

    def set_stats(self, *, correct: int, incorrect: int) -> None:
        self._stats_label.config(text=f"Правильно: {correct} | Неправильно: {incorrect}")

    def set_translator_button_state(self, state: str) -> None:
        self._show_translator_button.config(state=state)

    def start_timer(self) -> None:
        self._timer.start()
